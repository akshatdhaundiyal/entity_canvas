from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class JoinType(str, Enum):
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FULL = "FULL"

class Column(BaseModel):
    table: str
    column: str
    alias: Optional[str] = None

class JoinCondition(BaseModel):
    left: str  # e.g., "users.id"
    right: str # e.g., "orders.user_id"

class Join(BaseModel):
    type: JoinType
    table: str
    on: Union[str, JoinCondition]

class Operator(str, Enum):
    EQ = "="
    NE = "!="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    LIKE = "LIKE"
    IN = "IN"

class Condition(BaseModel):
    column: str
    operator: Operator
    value: Any
    logic: Optional[str] = "AND" # AND/OR for combining with next condition

class SortCondition(BaseModel):
    column: str
    direction: str = "ASC"  # ASC or DESC

class QueryAST(BaseModel):
    select: List[Column]
    from_table: str = Field(..., alias="from")
    joins: Optional[List[Join]] = []
    where: Optional[List[Condition]] = []
    sorts: Optional[List[SortCondition]] = []
    limit: Optional[int] = 100

    class Config:
        populate_by_name = True
