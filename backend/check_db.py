import asyncio
from sqlalchemy import text
from database import engine

async def check_tables():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
        tables = result.fetchall()
        print(f"Tables in 'public' schema: {tables}")

if __name__ == "__main__":
    asyncio.run(check_tables())
