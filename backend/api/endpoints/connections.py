from fastapi import APIRouter
from config import settings

router = APIRouter()

@router.get("")
async def list_connections():
    """List all configured database connection aliases."""
    return {"connections": list(settings.get_all_connections().keys())}
