# Technical Knowledge Base

## Hurdle: PowerShell `mkdir` Parameter Errors
- **Problem**: In powershell, the Linux/Unik `mkdir -p dir1 dir2` syntax often fails when combined with multiple paths or specific flag orders in some environments, leading to "A positional parameter cannot be found" errors.
- **Cause**: PowerShell's `mkdir` is an alias for `New-Item -ItemType Directory`, which handles multiple arguments differently than the GNU `mkdir`.
- **Solution**: Use `New-Item -ItemType Directory -Path ...` or, in automated agent scripts, create files using `write_to_file` which automatically creates parent directories in a cross-platform way.

## Hurdle: `npx nuxi init` Interactivity
- **Problem**: `nuxi init` prompted for template selection and module installation, which hangs automated agents.
- **Cause**: Default initialization is interactive.
- **Solution**: Use explicit flags: `nuxi init <dir> -t minimal --packageManager npm --no-gitInit --no-install`.

## Decision: Migrating to `uv` for Backend Management
- **Why**: `uv` is significantly faster than `pip` and provides a unified `pyproject.toml` based workflow that is more robust than `requirements.txt`.
- **Impact**: Backend builds are now optimized for Docker and local development. The `uv.lock` file ensures reproducible environments.
- **Constraints**: Developers must have `uv` installed, but the Dockerfile handles this automatically via a multi-stage build (`COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/`).

## Hydration & CORS Constraints
- **CORS**: The Nuxt 4 frontend runs on a different port (3000) than the FastAPI backend (8000). 
- **Solution**: Integrated `CORSMiddleware` in `backend/main.py` allowing all origins during the current scaffolding phase. This will be restricted to specific domains in production.

## Hurdle: Backend `ModuleNotFoundError` (Import Paths)
- **Problem**: When running the FastAPI app with `uv run uvicorn main:app` from within the `backend/` directory, the application failed with `ModuleNotFoundError: No module named 'backend'`.
- **Cause**: The code used absolute imports like `from backend.models.query import ...`. When the working directory is `backend/`, the `backend` package itself is not in the path; only its children (`models`, `services`) are.
- **Solution**: Refactored imports to be local to the `backend` directory (e.g., `from models.query import ...`). This ensures the app runs correctly both in the Docker container (which sets `WORKDIR /app` inside the backend context) and during local development when running from the `backend/` folder.
- **Constraints**: If running the entire app from the root of the monorepo, `PYTHONPATH` would need to include the `backend` folder, or imports would need to remain absolute. The current decision favors a modular approach where the backend can be run independently without monorepo-level path logic.

## Hurdle: uv Task Execution (`program not found`)
- **Problem**: User encountered `unrecognized subcommand 'main:app'` or `error: Failed to spawn: dev` when trying to run the app via `uv run`.
- **Cause**: `uv run` expects a binary from the environment (like `uvicorn`) or a script defined in `[project.scripts]`. It does not natively interpret `main:app` as a uvicorn module string.
- **Solution**: 
  1. Configured `[project.scripts]` in `backend/pyproject.toml` with `dev = "main:start"`.
  2. Created a `start()` entry point in `backend/main.py` that handles the uvicorn configuration.
- **Workflow**: The project now supports the standardized command `uv run dev` from within the `backend/` directory.

## Hurdle: IDE "Cannot find module" Warnings
- **Problem**: The IDE (VS Code/Cursor) shows `Cannot find module 'fastapi'` and other warnings despite the app running correctly via `uv run`.
- **Cause**: The IDE's Python extension defaults to the system Python interpreter instead of the `uv` virtual environment located at `backend/.venv`.
- **Solution**: Established a multi-root workspace using **[entity_canvas.code-workspace](file:///d:/self_work/projects/entity_canvas/entity_canvas.code-workspace)**. This unifies the backend and frontend settings into a single file and ensures that `python.defaultInterpreterPath` and Tailwind CSS associations are correctly applied when the workspace is opened. 
- **User Action**: To get the best experience, open the `entity_canvas.code-workspace` file and click **"Open Workspace"** in the bottom right (or go to `File > Open Workspace from File...`).

## Hurdle: Vue 3 Syntax Error (`$arguments`)
- **Problem**: Attempting to use `@event="handler($event, $arguments[0])"` in a Vue 3 template caused a "Property '$arguments' does not exist" error.
- **Cause**: `$arguments` is not a globally available template variable in Vue 3 (Nuxt 4).
- **Solution**: Refactored the child component to emit multiple arguments `emit('drag-column', event, data)` and the parent to use the direct handler reference `@drag-column="handleDragStart"`.

## Hurdle: Tailwind CSS "Unknown at rule" Warnings
- **Problem**: The IDE shows warnings for `@tailwind`, `@apply`, and other PostCSS rules in `.css` files.
- **Cause**: The IDE's default CSS service does not understand Tailwind-specific directives.
- **Solution**: Created `frontend/.vscode/settings.json` and set `"*.css": "tailwindcss"` in `files.associations` to tell the editor to use the Tailwind CSS language service for these files.

## Hurdle: Nuxt 4 Root Layout (`<NuxtWelcome />`)
- **Problem**: Accessing the root page displayed the default Nuxt info/welcome screen instead of the project's builder interface.
- **Cause**: The default `app.vue` generated by some Nuxt templates includes the `<NuxtWelcome />` component, which shadows the `pages/` directory.
- **Solution**: Replaced `<NuxtWelcome />` with `<NuxtPage />` in `frontend/app/app.vue`.

## Hurdle: Port Conflict (3000 vs 3001)
- **Problem**: Nuxt dev server started on port 3001 instead of the default 3000.
- **Cause**: Port 3000 was held by a previous background process or a hanging terminal session.
- **Solution**: Noted the change in URL to [http://localhost:3001](http://localhost:3001). For production/final dev, the previous process can be terminated.
