from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Chatbot Backend"
    app_env: str = "development"
    openai_api_key: str | None = None
    google_sheets_credentials_path: str | None = None

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
