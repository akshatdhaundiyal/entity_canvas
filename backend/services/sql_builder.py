import sqlglot
from sqlglot import exp, parse_one
from models.query import QueryAST, JoinType, Operator

def build_sql_from_ast(ast: QueryAST) -> str:
    """
    Transpiles the QueryAST into a PostgreSQL string using SQLGlot.
    """
    # Initialize the SELECT expression
    query = exp.select(*[
        exp.column(col.column, table=col.table).as_(col.alias) if col.alias else exp.column(col.column, table=col.table)
        for col in ast.select
    ]).from_(ast.from_table)

    # Add Joins
    if ast.joins:
        for join in ast.joins:
            if isinstance(join.on, str):
                on_clause = join.on
            else:
                on_clause = f"{join.on.left} = {join.on.right}"
            
            query = query.join(
                join.table,
                on=on_clause,
                join_type=join.type.value
            )

    # Add Where clauses
    if ast.where:
        where_expression = None
        for cond in ast.where:
            # Create the basic condition (e.g., column = value)
            # Use SQLGlot's safe value wrapping
            col_parts = cond.column.split('.')
            if len(col_parts) == 2:
                col_exp = exp.column(col_parts[1], table=col_parts[0])
            else:
                col_exp = exp.column(cond.column)
            
            # Use parse_one or specific expression builders to ensure safety
            # For simplicity in this scaffold, we use the literal wrapper
            val_exp = exp.Literal.string(str(cond.value)) if isinstance(cond.value, str) else exp.Literal.number(cond.value)
            
            new_cond = exp.EQ(this=col_exp, expression=val_exp)
            # Map other operators if needed...
            if cond.operator == Operator.GT:
                new_cond = exp.GT(this=col_exp, expression=val_exp)
            elif cond.operator == Operator.LT:
                new_cond = exp.LT(this=col_exp, expression=val_exp)
            # ... and so on

            if where_expression is None:
                where_expression = new_cond
            else:
                if cond.logic == "OR":
                    where_expression = exp.Or(this=where_expression, expression=new_cond)
                else:
                    where_expression = exp.And(this=where_expression, expression=new_cond)
        
        if where_expression:
            query = query.where(where_expression)

    # Add Sorting
    if ast.sorts:
        for sort in ast.sorts:
            query = query.order_by(f"{sort.column} {sort.direction}")

    # Add Limit
    if ast.limit:
        query = query.limit(ast.limit)

    # Transpile to Postgres dialect
    return query.sql(dialect="postgres")
