from fastapi import FastAPI
from app.core.config import get_settings
from app.core.logger import get_logger
from app.api import chat, leads

settings = get_settings()
logger = get_logger()

app = FastAPI(title=settings.app_name)

# Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(leads.router, prefix="/api", tags=["Leads"])

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": f"Welcome to {settings.app_name}!"}
