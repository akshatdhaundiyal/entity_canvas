import asyncio
from sqlalchemy import text
from database import engine

async def test_connection():
    try:
        print(f"Testing connection to: {engine.url}")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Connection successful! Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {str(e)}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
