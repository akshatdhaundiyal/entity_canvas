from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "dev_secret_key_change_me_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    bootstrap_secret: Optional[str] = None

    @field_validator("database_url", mode="before")
    @classmethod
    def ensure_async_driver(cls, v: str) -> str:
        """SQLAlchemy async requires the +asyncpg driver prefix. This auto-adds it."""
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()