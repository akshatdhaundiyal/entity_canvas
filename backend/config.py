import os
import re
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv, dotenv_values

# Find the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Load .env file explicitly using absolute path for os.environ
load_dotenv(os.path.join(basedir, '.env'), override=True)

class Settings(BaseSettings):
    database_url: Optional[str] = None
    
    secret_key: str = "dev_secret_key_change_me_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    bootstrap_secret: Optional[str] = None
    allowed_origins: list[str] = ["*"]  # Default to allow all for dev

    @staticmethod
    def harden_url(v: str) -> str:
        """
        Hardens the database URL for async compatibility.
        """
        if not v:
            return v
            
        # 1. Ensure driver is postgresql+asyncpg
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
            
        # 2. Fix SSL mode parameter (SQLAlchemy asyncpg wants 'ssl' not 'sslmode')
        if "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=", 1)
            
        # 3. Strip problematic libpq parameters
        for param in ["channel_binding", "target_session_attrs"]:
            v = re.sub(rf'[?&]{param}=[^&]*', '', v)

        # 4. Clean up trailing separators
        v = v.rstrip('?&')
            
        return v

    @field_validator("database_url", mode="before")
    @classmethod
    def ensure_async_driver(cls, v: str) -> str:
        return cls.harden_url(v)

    def get_all_connections(self) -> dict:
        """
        Dynamically discovers database connections from environment variables and the local .env file.
        Searches only in the backend folder for consistency.
        """
        conns = {}
        
        # 1. Look for .env ONLY in the backend folder (script directory)
        env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
        
        all_vars = {}
        if os.path.exists(env_path):
            all_vars.update(dotenv_values(env_path))
        
        # OS Environment variables must ALWAYS override .env files
        all_vars.update(dict(os.environ))
        
        # 2. Scan for dynamic DATABASE_URL_* keys
        for key, value in all_vars.items():
            if key and key.startswith("DATABASE_URL_") and key != "DATABASE_URL":
                alias = key.replace("DATABASE_URL_", "").lower().capitalize()
                if value:
                    conns[alias] = self.harden_url(str(value))
        
        return dict(sorted(conns.items()))

    class Config:
        env_file = ".env"
        extra = "allow" # Allow extra fields like DATABASE_URL_PAGILA to be captured

settings = Settings()