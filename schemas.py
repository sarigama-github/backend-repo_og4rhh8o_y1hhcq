from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime

# Collection: user (role-based access if needed later)
class User(BaseModel):
    email: str
    name: str
    role: Literal["admin", "project_manager", "team", "marketing"] = "team"
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Collection: sigil (strategic goals)
class Sigil(BaseModel):
    name: str
    intention: str
    image_url: Optional[HttpUrl] = None
    status: Literal["active", "achieved", "abandoned"] = "active"
    kpi_keys: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Collection: ritual_log (decision log)
class RitualLog(BaseModel):
    sigil_id: Optional[str] = None
    title: str
    notes: str
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None

# Collection: lead (website contact/quote requests)
class Lead(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None
    service: Optional[str] = None
    source: str = "website"
    created_at: Optional[datetime] = None

# Collection: blog_post
class BlogPost(BaseModel):
    title: str
    slug: str
    summary: Optional[str] = None
    content: str
    service_tags: List[str] = []
    keywords: List[str] = []
    cover_image_url: Optional[HttpUrl] = None
    published: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Collection: project
class Project(BaseModel):
    name: str
    client: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Literal["planned", "active", "paused", "completed", "archived"] = "planned"
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Collection: equipment (for QR talismans)
class Equipment(BaseModel):
    code: str  # QR code text / unique identifier
    name: str
    safety_notes: Optional[str] = None
    maintenance_history: List[Dict[str, Any]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Collection: checklist (safety acknowledgements)
class ChecklistAck(BaseModel):
    project_id: Optional[str] = None
    worker_name: str
    step: str
    signature_data_url: Optional[str] = None  # base64 PNG from canvas
    acknowledged_at: Optional[datetime] = None

# Collection: ticket (glitch management)
class Ticket(BaseModel):
    project_id: Optional[str] = None
    title: str
    severity: Literal["low", "medium", "high", "critical"] = "low"
    description: Optional[str] = None
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    root_cause: Optional[str] = None
    corrective_actions: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
