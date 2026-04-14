# Design Doc 01: Project Scaffolding & Architecture

## Overview
Status: **COMPLETED**
Milestone: 0
Impact: Core Foundation

This document defines the architectural foundation for **Entity Canvas**, a Visual SQL Builder. The goal was to establish a monorepo that separates concerns while maintaining a unified language (Query AST).

## Walkthrough

### 1. The Query AST (Shared Language)
The backbone of the application is a JSON-based Abstract Syntax Tree (AST). It is defined as a series of Pydantic models on the backend and an interface on the frontend.
- **Select**: List of objects `{table, column, alias}`.
- **Where**: List of objects `{column, operator, value, logic}`.
- **From/Joins**: Defined keys for the base table and related joints.

### 2. Backend (FastAPI + uv)
The backend uses **uv** for high-performance dependency management and task execution.
- **Packaging**: The backend is configured as a formal Python package (`tool.uv.package = true`) using the `hatchling` build-backend in a flat-layout configuration.
- **Task Runner**: A standardized `dev` script is defined in `pyproject.toml`, allowing the server to be started via `uv run dev`. This command triggers the `main:start` entry point with hot-reload enabled.
- **SQLGlot Service**: A dedicated service (`services/sql_builder.py`) takes the Pydantic AST and programmatically builds a SQL expression using the SQLGlot library, ensuring it follows **PostgreSQL** dialect and prevents injection.
- **Execute Endpoint**: A POST endpoint receives the AST, transpiles it, and returns mock results and the generated SQL.

### 3. Frontend (Nuxt 4 + Pinia)
A modern, dark-mode UI with glassmorphism effects.
- **Pinia Store**: Manages `currentQuery`.
- **Components**: 
  - `TableRegistry`: Draggable columns.
  - `DropZone`: Interactive select/filter areas.
  - `ResultTable`: Dynamic data display.

## Verification

| Test Case | Description | Expected Result | Status |
|-----------|-------------|-----------------|--------|
| AST Validation | Send invalid JSON to `/api/query/execute` | 422 Unprocessable Entity | ✅ Pass |
| SQL Generation | Drag `users.name` to Select | `SELECT users.name FROM users` | ✅ Pass |
| Filter Logic | Add `age > 18` | `WHERE users.age > 18` | ✅ Pass |
| Monorepo Check | Verify directories exist | `backend/` and `frontend/` are separate | ✅ Pass |
| uv Run Dev | Execute `uv run dev` | Server starts with hot-reload | ✅ Pass |
| IDE Module Search | Check IDE for module errors | No red underlines (with .vscode config) | ✅ Pass |
