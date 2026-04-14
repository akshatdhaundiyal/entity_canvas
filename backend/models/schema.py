from pydantic import BaseModel
from typing import List, Optional

class ColumnMetadata(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    default_value: Optional[str] = None

class TableMetadata(BaseModel):
    name: str
    columns: List[ColumnMetadata]

class DatabaseSchema(BaseModel):
    tables: List[TableMetadata]
