# Coding Standards

## Backend (FastAPI + uv)
- **Dependency Management**: Use `uv` exclusively. No `requirements.txt`.
- **Workflow**: Use `uv run dev` from the `backend/` directory to start the server.
- **Validation**: All API endpoints MUST use Pydantic models for request/response validation.
- **IDE Sync**: Every backend project MUST include a `.vscode/settings.json` pointing to the local `.venv`.
- **SQL Building**: Use **SQLGlot** for all SQL generation. Target the `postgres` dialect.
- **Async**: Use asynchronous drivers (`asyncpg`, `sqlalchemy[asyncio]`) for database communication.
- **Testing**: Maintain a high coverage for SQL transpilation logic.

## Frontend (Nuxt 4 + Tailwind)
- **Convention**: Follow the Nuxt 4 directory structure and composable patterns.
- **State**: Use **Pinia** for cross-component state (like the Query AST).
- **Styling**: Use Tailwind CSS with a focus on modern aesthetics (Glassmorphism, dark mode).
- **Draggable**: Use `vuedraggable` for interaction-heavy components.
- **Type Safety**: Use TypeScript for all store and component logic.

## Database (PostgreSQL)
- **Dialect**: Always target PostgreSQL 15+.
- **Safety**: Ensure all queries are parameterized by the transpiler.
