# Entity Canvas: Backend

The high-performance **FastAPI** backend for Entity Canvas. It handles database schema discovery, Query AST validation, and SQL transpilation via **SQLGlot**.

## 🚀 Built With
- **Framework**: FastAPI (Pydantic V2)
- **Dependency Manager**: **uv**
- **Transpilation**: SQLGlot (PostgreSQL Dialect)
- **Database**: SQLAlchemy (Async) with `asyncpg`

## 📂 Structure
- `models/`: Pydantic definitions for the Query AST and Database Schema.
- `services/`: Core logic for SQL building and schema introspection.
- `main.py`: API entry point and orchestration.

## 🛠️ Development
We use **uv** for managing the Python environment.
```bash
# Install dependencies & create venv
uv sync

# Start development server with hot-reload
uv run dev
```

For detailed architectural information, see the **[Query Engine Design Doc](file:///d:/self_work/projects/entity_canvas/docs/design_docs/02_query_engine.md)**.
