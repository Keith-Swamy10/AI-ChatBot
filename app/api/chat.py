from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    # Placeholder logic — will later include FAISS + LLM
    user_message = payload.message
    # For now, just echo back
    reply = f"You said: {user_message}"
    return ChatResponse(reply=reply)
