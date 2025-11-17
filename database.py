import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[AsyncIOMotorClient] = None
_db = None

async def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(DATABASE_URL, serverSelectionTimeoutMS=3000)
    return _client

async def get_db():
    global _db
    if _db is None:
        client = await get_client()
        _db = client[DATABASE_NAME]
    return _db

async def ping_db() -> Dict[str, str]:
    try:
        client = await get_client()
        # Attempt a server selection/ping
        await client.admin.command('ping')
        return {
            "status": "ok",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
        }
    except ServerSelectionTimeoutError:
        return {
            "status": "unreachable",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
        }
    except Exception as e:
        return {
            "status": f"error: {e}",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
        }

async def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    try:
        db = await get_db()
        now = datetime.utcnow()
        data["created_at"] = data.get("created_at", now)
        data["updated_at"] = data.get("updated_at", now)
        res = await db[collection_name].insert_one(data)
        return str(res.inserted_id)
    except Exception as e:
        # Propagate a clear error string; caller can format response
        raise RuntimeError(f"Database write failed: {e}")

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 100) -> List[Dict[str, Any]]:
    try:
        db = await get_db()
        cursor = db[collection_name].find(filter_dict or {}).limit(limit)
        docs: List[Dict[str, Any]] = []
        async for d in cursor:
            d["_id"] = str(d.get("_id"))
            docs.append(d)
        return docs
    except Exception:
        # Graceful fallback when DB is unavailable
        return []
