import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.schema import DatabaseSchema
from services.schema_discovery import get_database_schema

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", response_model=DatabaseSchema)
async def get_schema(db: AsyncSession = Depends(get_db)):
    """Discover the schema for the active database."""
    try:
        return await get_database_schema(db)
    except Exception as e:
        logger.error(f"Error discovering schema: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
