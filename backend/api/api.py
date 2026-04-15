from fastapi import APIRouter
from api.endpoints import connections, schema, queries

api_router = APIRouter()

api_router.include_router(connections.router, prefix="/connections", tags=["connections"])
api_router.include_router(schema.router, prefix="/schema", tags=["schema"])
api_router.include_router(queries.router, prefix="/query", tags=["queries"])
