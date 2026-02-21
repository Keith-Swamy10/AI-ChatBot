from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.leads.lead_extractor import process_lead_input, get_lead_by_session_id

router = APIRouter()

class LeadRequest(BaseModel):
    session_id: str
    user_message: str

class LeadResponse(BaseModel):
    status: str
    message: str
    lead_completed: bool = False

@router.post("/lead", response_model=LeadResponse)
async def add_lead(payload: LeadRequest):
    """
    Process user input for lead capture.
    Handles name, email, phone collection and Google Sheets integration.
    """
    result = process_lead_input(payload.session_id, payload.user_message)
    
    return LeadResponse(
        status="success" if result["handled"] else "skipped",
        message=result["message"],
        lead_completed=result.get("lead_completed", False)
    )

@router.get("/lead/{session_id}")
async def get_lead(session_id: str):
    """
    Retrieve complete lead data for a session.
    """
    lead = get_lead_by_session_id(session_id)
    
    if not lead:
        return {"status": "not_found", "data": None}
    
    return {"status": "success", "data": lead}
