# Milestone 06: Backend Refactoring & Hardening

## Objective
Improve the maintainability, security, and testability of the backend by modularizing routes, centralizing error handling, and implementing safety constraints on SQL generation.

## Technical Implementation

### Modular Router Architecture
- **Restructuring**: Moved all API endpoints from `main.py` into a versioned structure in `backend/api/`.
- **Endpoints**: Created dedicated routers for `connections`, `schema`, and `queries`.
- **Aggregation**: A central `api_router` in `backend/api/api.py` includes all sub-routers, simplifying the main application entry point.

### Security Hardening
- **SELECT-only Constraint**: Implemented a validation check in `backend/services/sql_builder.py` that raises a `QueryValidationError` if the generated SQL is not a `SELECT` statement. This prevents destructive operations via the visual builder.
- **Configurable CORS**: Added `allowed_origins` to the `Settings` class in `backend/config.py`, allowing for restricted cross-origin access in production while maintaining a flexible default for development.

### Standardized Error Handling
- **Custom Exceptions**: Defined a hierarchy of application-centric exceptions in `backend/core/exceptions.py` (e.g., `DatabaseConnectionError`, `QueryValidationError`).
- **Global Handler**: Implemented a global exception handler in `backend/main.py` that catches `AppException` and returns standardized JSON responses with error messages and details.

### Testing Strategy
- **Framework**: Integrated `pytest` and `httpx` for integration testing.
- **Base Config**: Created `backend/tests/conftest.py` with reusable fixtures for the test client and standard mock data.
- **Initial Suite**: Added core integration tests in `backend/tests/test_queries.py` to ensure endpoint reliability.

## Technical Hurdles & Learnings
- **FastAPI Lifespan Events**: Noted that `on_event("startup")` is deprecated. While currently using it for simplicity, future refactoring should move to lifespan handlers.
- **SQLGlot Safety**: While `SQLGlot` is powerful for transpilation, it doesn't automatically restrict the *type* of operation (e.g., SELECT vs DELETE). Manual string prefix checking served as a reliable fallback for this milestone's read-only requirement.
- **Dependency Management**: Adding `pytest` and `httpx` required updating the `pyproject.toml` and verified that `uv sync` correctly handles new testing dependencies in the lockfile.

## State Change Checklist
- [x] Utility scripts moved to `backend/scripts/`.
- [x] Dependencies updated in `pyproject.toml`.
- [x] Custom exceptions and global handler implemented.
- [x] API routers modularized and tags added for Swagger UI.
- [x] SELECT-only validation added to SQL builder.
- [x] Basic test suite implemented and passing.
