# Entity Canvas Features

## Core Functionality
- [x] **Visual SQL Builder**: Drag and drop table columns to build SELECT and WHERE clauses.
- [x] **SQL Transpilation**: Real-time generation of PostgreSQL-compatible SQL using SQLGlot.
- [x] **Query Execution**: POST endpoint to execute generated SQL and return data.
- [x] **Interactive Schema Browser**: Sidebar with available tables and columns.
- [x] **Live Preview**: Syntax-highlighted SQL preview in the UI.
- [x] **Result Visualization**: Modern table layout for displaying query results.

## Technical Highlights
- **Backend**: FastAPI with Pydantic validation, SQLGlot safety, and **uv** for dependency management.
- **Frontend**: Nuxt 4 (Vue 3) with Pinia state management and Tailwind CSS.
- **Security**: Parameterized/Validated SQL generation to prevent injection.
- **Aesthetics**: Premium dark-mode interface with glassmorphism effects.
- **DevOps**: Docker Compose for orchestration, with `uv` optimized Docker builds.

## Roadmap
- [ ] Support for complex JOIN logic (UI refined).
- [ ] Aggregations (GROUP BY, HAVING).
- [ ] Order By and Limit.
- [ ] Real PostgreSQL connection integration with SQLAlchemy.
