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
        """
        Hardens the database URL for async compatibility:
        1. Auto-adds the +asyncpg driver prefix if missing.
        2. Converts 'sslmode=require' to 'ssl=require' (required by asyncpg).
        """
        if not v:
            return v
            
        # 1. Fix Driver
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        # 2. Fix SSL parameter name (sslmode -> ssl)
        if "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=", 1)
            
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()