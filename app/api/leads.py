from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LeadRequest(BaseModel):
    name: str
    email: str
    phone: str | None = None

class LeadResponse(BaseModel):
    status: str
    message: str

@router.post("/lead", response_model=LeadResponse)
async def add_lead(payload: LeadRequest):
    # Placeholder logic — will later push to Google Sheets or DB
    print(f"New lead received: {payload}")
    return LeadResponse(status="success", message="Lead captured successfully!")
