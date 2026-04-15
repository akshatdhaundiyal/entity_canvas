from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
import re

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
        3. Strips incompatible libpq parameters (channel_binding, target_session_attrs).
        """
        if not v:
            return v
            
        # 1. Fix Driver (postgresql:// -> postgresql+asyncpg://)
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        # 2. Fix SSL parameter name (sslmode -> ssl)
        if "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=", 1)
            
        # 3. Strip incompatible parameters that cause asyncpg to crash
        # These are standard in libpq (and Neon strings) but unhandled by asyncpg
        incompatible_params = ["channel_binding", "target_session_attrs"]
        for param in incompatible_params:
            # Matches ?param=val or &param=val
            v = re.sub(rf'[?&]{param}=[^&]*', '', v)

        # 4. Clean up URL (handle case where stripping left a trailing '?' or '&')
        v = v.rstrip('?&')
        # If we stripped the first param after '?', replace subsequent '&' with '?'
        if "?" not in v and "ssl=" in v:
             v = v.replace("ssl=", "?ssl=", 1)
            
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()