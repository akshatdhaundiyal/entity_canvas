import sys

try:
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from models.query import QueryAST
    from services.sql_builder import build_sql_from_ast
    from services.schema_discovery import get_database_schema
    from models.schema import DatabaseSchema
    from database import get_db
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import text
    import logging
    import os
except ImportError as e:
    sys.exit(1)

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Entity Canvas API")

# Configure CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    from config import settings
    logger.info("--------------------------------------------------")
    logger.info("🚀 Entity Canvas Backend is starting up!")
    logger.info(f"📡 Environment: PORT={os.getenv('PORT', '8080')}")
    # Mask the password in the URL before logging
    db_url = settings.database_url
    if "@" in db_url:
        safe_url = db_url.split("@")[-1]
        logger.info(f"🔗 Database Host: {safe_url}")
    else:
        logger.info(f"🔗 Database URL: {db_url}")
    logger.info("--------------------------------------------------")

@app.get("/")
async def root():
    return {"message": "Visual SQL Builder API is running"}

@app.get("/api/schema", response_model=DatabaseSchema)
async def get_schema(db: AsyncSession = Depends(get_db)):
    try:
        return await get_database_schema(db)
    except Exception as e:
        logger.error(f"Error discovering schema: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query/execute")
async def execute_query(ast: QueryAST, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Transpile AST to SQL
        sql = build_sql_from_ast(ast)
        logger.info(f"Generated SQL: {sql}")

        # 2. Execute SQL against PostgreSQL
        result = await db.execute(text(sql))
        
        # Convert rows to dictionaries for JSON response
        # result.mappings() provides a dictionary-like interface for each row
        rows = [dict(row) for row in result.mappings()]

        return {
            "sql": sql,
            "results": rows,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start():
    """Launched with `uv run dev` or direct `python main.py`"""
    try:
        import uvicorn
        import os
        
        port = int(os.getenv("PORT", 8000))
        host = "0.0.0.0"
        reload = os.getenv("PORT") is None # Disable reload in production
        
        uvicorn.run("main:app", host=host, port=port, reload=reload)
    except Exception as e:
        print(f"❌ FATAL ERROR during server startup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start()
