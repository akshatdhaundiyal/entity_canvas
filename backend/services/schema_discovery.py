from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.schema import DatabaseSchema, TableMetadata, ColumnMetadata
from typing import Dict, List

async def get_database_schema(db: AsyncSession) -> DatabaseSchema:
    """
    Discovers the database schema by querying common PostgreSQL system catalogs.
    Focuses on the 'public' schema and base tables only.
    """
    # Query to fetch all columns for base tables in the public schema
    query = text("""
        SELECT 
            table_name, 
            column_name, 
            data_type, 
            is_nullable, 
            column_default 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
          AND table_name IN (
              SELECT table_name 
              FROM information_schema.tables 
              WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
          )
        ORDER BY table_name, ordinal_position;
    """)

    result = await db.execute(query)
    rows = result.mappings()

    # Organize columns by table
    tables_map: Dict[str, List[ColumnMetadata]] = {}
    
    for row in rows:
        table_name = row['table_name']
        column = ColumnMetadata(
            name=row['column_name'],
            data_type=row['data_type'],
            is_nullable=row['is_nullable'] == 'YES',
            default_value=str(row['column_default']) if row['column_default'] is not None else None
        )
        
        if table_name not in tables_map:
            tables_map[table_name] = []
        tables_map[table_name].append(column)

    # Convert to DatabaseSchema model
    tables_list = [
        TableMetadata(name=name, columns=cols) 
        for name, cols in tables_map.items()
    ]
    
    return DatabaseSchema(tables=tables_list)
