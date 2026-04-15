import sys
import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.exceptions import AppException
from api.api import api_router
from config import settings

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Entity Canvas API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("--------------------------------------------------")
    logger.info("🚀 Entity Canvas Backend is starting up!")
    logger.info(f"📡 Environment: PORT={os.getenv('PORT', '8080')}")
    
    conns = settings.get_all_connections()
    for alias, url in conns.items():
        if "@" in url:
            safe_url = url.split("@")[-1]
            logger.info(f"🔗 Database connection '{alias}': {safe_url}")
        else:
            logger.info(f"🔗 Database connection '{alias}': {url}")
    logger.info("--------------------------------------------------")

# Exception Handler for custom application exceptions
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "details": exc.details
        },
    )

# Include Modular Routers
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Visual SQL Builder API (v1) is running"}

def start():
    """Launched with `uv run dev` or direct `python main.py`"""
    try:
        import uvicorn
        port = int(os.getenv("PORT", 8000))
        host = "0.0.0.0"
        reload = os.getenv("PORT") is None # Disable reload in production
        
        uvicorn.run("main:app", host=host, port=port, reload=reload)
    except Exception as e:
        print(f"❌ FATAL ERROR during server startup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start()
