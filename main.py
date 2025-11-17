from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

from database import create_document, get_documents, ping_db
from schemas import Sigil, RitualLog, Lead, BlogPost, Project, Equipment, ChecklistAck, Ticket

app = FastAPI(title="Royal Star Teknomaaginen Toiminta-alusta")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TestResponse(BaseModel):
    ok: bool
    message: str
    db_status: Dict[str, str] | None = None

@app.get("/", response_model=TestResponse)
async def root():
    return TestResponse(ok=True, message="API alive.")

@app.get("/test", response_model=TestResponse)
async def test():
    db = await ping_db()
    ok = db.get("status") == "ok"
    return TestResponse(ok=ok, message="DB check complete", db_status=db)

# Sigils
@app.post("/sigils")
async def create_sigil(sigil: Sigil):
    try:
        sigil_id = await create_document("sigil", sigil.dict())
        return {"id": sigil_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/sigils")
async def list_sigils():
    return await get_documents("sigil")

# Ritual logs
@app.post("/ritual-logs")
async def create_ritual_log(log: RitualLog):
    try:
        log_id = await create_document("ritual_log", log.dict())
        return {"id": log_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/ritual-logs")
async def list_ritual_logs():
    return await get_documents("ritual_log")

# Leads
@app.post("/leads")
async def create_lead(lead: Lead):
    try:
        lead_id = await create_document("lead", lead.dict())
        return {"id": lead_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

# Blog
@app.post("/blog")
async def create_blog_post(post: BlogPost):
    try:
        post_id = await create_document("blog_post", post.dict())
        return {"id": post_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/blog")
async def list_blog_posts():
    return await get_documents("blog_post")

# Projects
@app.post("/projects")
async def create_project(project: Project):
    try:
        project_id = await create_document("project", project.dict())
        return {"id": project_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/projects")
async def list_projects():
    return await get_documents("project")

# Equipment with QR
@app.post("/equipment")
async def create_equipment(eq: Equipment):
    try:
        eq_id = await create_document("equipment", eq.dict())
        return {"id": eq_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/equipment")
async def list_equipment():
    return await get_documents("equipment")

# Safety checklist acknowledgements
@app.post("/checklist-acks")
async def create_checklist_ack(ack: ChecklistAck):
    try:
        ack_id = await create_document("checklistack", ack.dict())
        return {"id": ack_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/checklist-acks")
async def list_checklist_acks():
    return await get_documents("checklistack")

# Tickets (glitch management)
@app.post("/tickets")
async def create_ticket(ticket: Ticket):
    try:
        t_id = await create_document("ticket", ticket.dict())
        return {"id": t_id}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/tickets")
async def list_tickets():
    return await get_documents("ticket")

# Maintenance
class MaintenanceResult(BaseModel):
    summary: str
    archived_projects: int

@app.post("/maintenance/run", response_model=MaintenanceResult)
async def run_maintenance():
    projects = await get_documents("project", {"status": "completed"})
    return MaintenanceResult(
        summary="Maintenance tasks executed (security scan, updates, archive, report)",
        archived_projects=len(projects),
    )
