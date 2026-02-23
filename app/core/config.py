from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_DATABASENAME = os.getenv("DB_DATABASENAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

class Settings(BaseSettings):
    app_name: str = "AI Chatbot Backend"
    app_env: str = "development"
    
    # Database
    db_host: str = DB_HOSTNAME
    db_user: str = DB_USERNAME
    db_password: str = DB_PASSWORD
    db_name: str = DB_DATABASENAME
    
    # Google Sheets
    google_service_account_file: str | None = GOOGLE_SERVICE_ACCOUNT_FILE
    google_sheet_id: str | None = GOOGLE_SHEET_ID
    
    # Azure OpenAI
    azure_openai_endpoint: str | None = AZURE_OPENAI_ENDPOINT
    openai_api_key: str | None = OPENAI_API_KEY

    model_config = ConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
