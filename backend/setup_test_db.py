import asyncio
from sqlalchemy import text
from database import engine

async def setup_db():
    async with engine.begin() as conn:
        print("Creating test tables...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'draft',
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """))
        print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(setup_db())
