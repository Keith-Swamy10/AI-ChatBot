from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Chatbot Backend"
    app_env: str = "development"
    
    # Database
    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "chatbot_db"
    
    # Google Sheets
    google_service_account_file: str | None = None
    google_sheet_id: str | None = None
    
    # Azure OpenAI
    azure_openai_endpoint: str | None = None
    openai_api_key: str | None = None

    model_config = ConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
