# Knowledge Base 01: Scaffolding & Core Architecture

This document captures the distilled learnings, "gotchas," and technical hurdles identified during the scaffolding phase of **Entity Canvas**.

## Hurdle: PowerShell `mkdir` Parameter Errors
- **Problem**: In powershell, `mkdir -p dir1 dir2` often fails with "A positional parameter cannot be found."
- **Learning**: PowerShell's `mkdir` is an alias for `New-Item`. It doesn't handle multiple positional arguments the same as GNU-mkdir.
- **Solution**: Use `New-Item -ItemType Directory -Path ...` or automate via specialized file-writing tools that handle parent directory creation.

## Hurdle: Migrating to `uv` for Backend Management
- **Context**: Transitioning from `pip` to **uv** for dependency management.
- **Learning**: `uv` is significantly faster but requires a `pyproject.toml` based workflow. It eliminates the need for `requirements.txt`.
- **Constraint**: The Dockerfile must be updated to use the `astral-sh/setup-uv` step or the Docker binary (`ghcr.io/astral-sh/uv:latest`).

## Decision: Backend Import Strategy
- **Issue**: `ModuleNotFoundError` when running FastAPI from the root or subfolders.
- **Learning**: Absolute imports (e.g., `from backend.models...`) break if the child directory is the execution context.
- **Solution**: Refactored to relative-style imports within the `backend` package. This allows the backend to be treated as a standalone module during Docker runs.

---

## Technical Definitions

| Term | Definition |
|------|------------|
| **Hydration** | The process where client-side JavaScript takes over a static HTML page sent by the server to make it interactive. |
| **Monorepo** | A software development strategy where code for many projects is stored in the same repository. |
| **Pydantic** | A data validation and settings management library for Python using type annotations. |

> [!TIP]
> **Hot-Reloading**: Use `uv run dev` during local development. It uses `uvicorn --reload` under the hood, ensuring every save reflects immediately in the API.
