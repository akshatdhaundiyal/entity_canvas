# Future Roadmap & Enhancements

This document outlines the planned features and architectural improvements for **Entity Canvas**.

## 🚀 Priority 1: Developer Experience (DX)

### 1. Unified CLI
Create a root-level Taskfile or Makefile to consolidate commands:
- `make dev`: Starts docker-compose.
- `make sync`: Runs backend migrations and frontend typegen.
- `make test`: Runs both backend (pytest) and frontend (vitest) tests.

### 2. Alembic Migrations
- Integrate **Alembic** to manage the `Local Pagila` schema.
- Implement an automated "Migration -> Sync" pipeline where running a migration automatically triggers `npm run typegen`.

## 🧠 Priority 2: Core Features

### 1. Visual Query Builder (V1)
- **Drag & Drop**: Ability to drag tables from the sidebar onto the canvas.
- **Auto-Join**: Automatically suggest joins based on Foreign Key relationships discovered in the schema.
- **Live Preview**: A bottom panel showing the first 10 rows of the current query state.

### 2. Schema Export
- Export the visual layout of the ER diagram as an SVG or PNG.
- Generate SQL `CREATE TABLE` scripts directly from the canvas.

## 🛠️ Priority 3: Architecture

### 1. Backend Security Hardening
- **Read-Only Mode**: Implement a strict "Read-Only" mode for specific connections to prevent accidental `DROP TABLE` or `DELETE` commands.
- **SQL Injection Guard**: Move beyond simple validation to a more robust AST-based SQL sanitizer.

### 2. Shared Type Automation
- Implement a Nuxt Module that polls the backend `/openapi.json` during development and updates types without manual command execution.

## 📈 Priority 4: Deployment

### 1. Production Docker Build
- Optimize the `Dockerfile` for production (multi-stage builds, non-root users, minified assets).
- Implement a CI/CD pipeline using GitHub Actions to deploy to a cloud provider.

## 🧪 Unique Innovations (The Competitive Edge)

### 1. Semantic Join Suggestions (AI-Powered)
- **Concept**: Move beyond Foreign Keys to "Data Discovery."
- **Implementation**: Analyze column names and data distributions to suggest joins between unrelated tables (e.g., matching `user_id` to `owner_guid`).

### 2. "SQL-to-Canvas" Reverse Engineering
- **Concept**: Instant visualization of legacy code.
- **Implementation**: Paste a raw SQL block and have SQLGlot parse it into a visual graph of nodes and edges on the canvas.

### 3. Visual Performance Heatmap
- **Concept**: "See" the bottlenecks.
- **Implementation**: Map `EXPLAIN ANALYZE` costs directly onto the canvas. High-cost joins appear as thick/red lines; sequential scans make tables glow.

### 4. Schema Evolution Impact Analysis
- **Concept**: Proactive breaking-change detection.
- **Implementation**: Simulate a schema change (like dropping a column) and immediately highlight all dependent queries or "saved canvases" that would fail.

### 5. Multi-Dialect Polyglot Export
- **Concept**: Unified interface for the modern data stack.
- **Implementation**: Toggle between Postgres, Snowflake, BigQuery, and DuckDB syntax for the same visual query using SQLGlot's transpilation layers.

---
*Last Updated: 2026-04-16*
