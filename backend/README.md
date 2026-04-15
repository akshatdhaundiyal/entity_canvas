# Entity Canvas: Backend

The high-performance **FastAPI** backend for Entity Canvas. It handles database schema discovery, Query AST validation, and SQL transpilation via **SQLGlot**.

## 🚀 Built With
- **Framework**: FastAPI (Pydantic V2)
- **Dependency Manager**: **uv**
- **Transpilation**: SQLGlot (PostgreSQL Dialect)
- **Database**: SQLAlchemy (Async) with `asyncpg`

## 📂 Structure
- `api/`: Modular routers for connections, schemas, and queries.
- `core/`: Application-wide components like exceptions and middleware.
- `models/`: Pydantic definitions for the Query AST and Database Schema.
- `services/`: Core logic for SQL building and schema introspection.
- `main.py`: Application entry point and initialization.
- `scripts/`: Utility scripts for database management and setup.

## 🛠️ Development
We use **uv** for managing the Python environment.
```bash
# Install dependencies & create venv
uv sync

# Start development server with hot-reload
uv run dev
```

## 🧪 Testing
We use **pytest** for integration testing.
```bash
# Run all tests
uv run pytest tests/
```

For detailed architectural information, see the **[Query Engine Design Doc](file:///d:/self_work/projects/entity_canvas/docs/design_docs/02_query_engine.md)**.
