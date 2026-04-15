# Milestone 05: Multi-Database Support

## Objective
Enable dynamic discovery and switching between multiple database environments (Local, Staging, Cloud) within the Entity Canvas workspace.

## Technical Implementation

### Dynamic Discovery Logic
The backend now implements an aggressive discovery pattern in `backend/config.py`:
- **Pattern**: Scans for all environment variables prefixed with `DATABASE_URL_`.
- **Location**: Strictly looks for `backend/.env` using absolute paths to prevent directory resolution issues.
- **Hardening**: Automatically sanitizes connection strings for `asyncpg` compatibility (driver prefix fix, SSL parameter normalization).

### Frontend State Management
- **Connection Store**: A new Pinia store (`connection.ts`) manages the active connection and available list.
- **Proactive Loading**: The list of available databases is fetched automatically upon store initialization with cache-busting logic.
- **Persistence**: The active database alias is synchronized with `localStorage` to survive page reloads.

### Redesigned Workspace UI
- **Unified Header**: Merged the database switcher, workspace metrics, and schema refresh into a single premium navbar.
- **Segmented Control**: Switched from a dropdown to a segmented button row for improved UI reliability and faster context switching.

## Technical Hurdles & Learnings
- **URL Mangling**: Standard libpq connection strings (especially from Neon) often contain parameters like `sslmode=require` or `channel_binding=require` which `asyncpg` rejects. Implemented a robust `harden_url` utility to clean these up transparently.
- **Component Resolution**: Discovered that certain Nuxt UI v3 components (like `UDropdown`) were failing to resolve in the current Nuxt UI v4 setup. Switched to `UButton` groups for the switcher, which solved both the resolution and the z-index clipping issues.
- **Environment Context**: Verified that `uv run` and `load_dotenv` require absolute path resolution to consistently find the `.env` file when the server is started from different working directories.

## State Change Checklist
- [x] Backend `GET /api/connections` endpoint implemented.
- [x] Automatic driver injection (`postgresql+asyncpg`) for all discovered URLs.
- [x] Workspace navbar merged and polished.
- [x] Selection state persisted in `localStorage`.
- [x] Segmented switcher replacing the problematic dropdown.
