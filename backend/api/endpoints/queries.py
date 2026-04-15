import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from models.query import QueryAST
from services.sql_builder import build_sql_from_ast

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/execute")
async def execute_query(ast: QueryAST, db: AsyncSession = Depends(get_db)):
    """Transpile an AST and execute the resulting SQL."""
    try:
        # 1. Transpile AST to SQL
        sql = build_sql_from_ast(ast)
        logger.info(f"Generated SQL: {sql}")

        # 2. Execute SQL against PostgreSQL
        result = await db.execute(text(sql))
        
        # Convert rows to dictionaries for JSON response
        rows = [dict(row) for row in result.mappings()]

        return {
            "sql": sql,
            "results": rows,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        # Check if it's our validation error or something else
        status_code = getattr(e, "status_code", 500)
        raise HTTPException(status_code=status_code, detail=str(e))
