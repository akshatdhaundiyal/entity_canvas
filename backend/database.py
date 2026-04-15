from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

DATABASE_URL = settings.database_url

if not DATABASE_URL:
    print("❌ ERROR: 'DATABASE_URL' is missing from settings.")
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
