import asyncio
import json
from database import SessionLocal
from services.schema_discovery import get_database_schema

async def test_discovery():
    print("Testing Schema Discovery Service...")
    async with SessionLocal() as db:
        try:
            schema = await get_database_schema(db)
            print("Successfully discovered schema:")
            # Use model_dump_json() for Pydantic V2
            print(schema.model_dump_json(indent=2))
        except Exception as e:
            print(f"Discovery failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_discovery())
