import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Smart Discovery: Automatically bridge localhost to host.docker.internal if in Docker
def resolve_database_url(url: str) -> str:
    if not url: return url
    # Check if inside Docker
    if os.path.exists("/.dockerenv") and "@localhost" in url:
        print("🐳 Docker environment detected: Automatically bridging 'localhost' to 'host.docker.internal'")
        return url.replace("@localhost", "@host.docker.internal")
    return url

DATABASE_URL = resolve_database_url(os.getenv("DATABASE_URL"))

if not DATABASE_URL:
    print("❌ ERROR: 'DATABASE_URL' environment variable is missing or empty.")
    raise ValueError("Missing DATABASE_URL")

# Create Async Engine
# echo=True will log all SQL expressions to stdout
engine = create_async_engine(DATABASE_URL, echo=True)

# Create SessionLocal class for creating database sessions
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    """
    Dependency to provide a database session to FastAPI endpoints.
    Ensures the session is closed after the request is finished.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
