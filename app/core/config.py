from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "Expense Tracker API"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # Database: prefer DATABASE_URL; fallback to SQLite
    database_url: Optional[str] = os.getenv("DATABASE_URL")

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return "sqlite:///./expense_tracker.db"


settings = Settings()
