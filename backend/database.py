from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from config import settings
from fastapi import Header
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self._engines: Dict[str, AsyncEngine] = {}
        self._session_factories: Dict[str, async_sessionmaker] = {}

    def get_engine(self, alias: str) -> AsyncEngine:
        all_conns = settings.get_all_connections()
        
        # Determine the correct alias to use
        if alias not in all_conns:
            # Fallback to 'Local' or the first available connection
            fallback = "Local" if "Local" in all_conns else (list(all_conns.keys())[0] if all_conns else None)
            if not fallback:
                raise ValueError("No database connections configured.")
            alias = fallback

        if alias not in self._engines:
            url = all_conns[alias]
            logger.info(f"🔗 Creating new engine for database: {alias}")
            self._engines[alias] = create_async_engine(url, echo=True)
            
        return self._engines[alias]

    def get_session_factory(self, alias: str) -> async_sessionmaker:
        if alias not in self._session_factories:
            engine = self.get_engine(alias)
            self._session_factories[alias] = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return self._session_factories[alias]

# Singleton instance
db_manager = DatabaseManager()

class Base(DeclarativeBase):
    pass

async def get_db(x_database_alias: Optional[str] = Header(None)):
    """
    Dependency to provide a database session based on the X-Database-Alias header.
    Defaults to 'Local' if the header is missing or invalid.
    """
    alias = x_database_alias or "Local"
    session_factory = db_manager.get_session_factory(alias)
    
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
