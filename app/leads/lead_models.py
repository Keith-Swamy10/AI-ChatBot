from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Lead(BaseModel):
    session_id: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    intent_summary: Optional[str] = None
    created_at: datetime = datetime.utcnow()


class LeadState(BaseModel):
    session_id: str
    current_step: str  
    # Possible values:
    # NONE | ASKED_NAME | ASKED_EMAIL | ASKED_PHONE | COMPLETED
    updated_at: datetime = datetime.utcnow()
