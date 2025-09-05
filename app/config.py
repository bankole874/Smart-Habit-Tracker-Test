# app/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://username:password@localhost/habit_tracker_db"
    secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
