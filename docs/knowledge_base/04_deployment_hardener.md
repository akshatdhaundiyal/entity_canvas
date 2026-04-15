# Lessons Learned: Backend Deployment & Infrastructure Hardening

This document captures the critical technical hurdles and successfully implemented solutions for the Entity Canvas backend.

## 1. Docker Networking: The "Localhost" Bridge [IMPLEMENTED]
### Problem
A containerized app trying to connect to a local database at `localhost:5432` will fail. Inside a container, `localhost` refers to the container itself, not the host machine.
### Solution
- **Action**: For **containerized local development**, we use **`host.docker.internal:5432`** in `backend/.env` to reach the Windows host.
- **Action**: For **local execution outside Docker** (e.g., `uv run`), we must use **`localhost`** or **`127.0.0.1`**.
- **Action**: We added the `extra_hosts` bridge to `docker-compose.yml` to ensure containers can resolve the host gateway.
- **Cloud Note**: Cloud Run ignores these local bridges and uses the Neon URL provided via GitHub Secrets.

## 2. Pydantic Settings V2 & `.env` Precision [IMPLEMENTED]
### Problem
Pydantic is extremely sensitive to `.env` formatting. Spaces around the equals sign (e.g., `VAR = val`) will cause the variable to be missed, leading to `ValidationError`.
### Solution
- **Action**: Re-formatted `.env` to strict `KEY=VALUE` format.
- **Action**: Provided a bootstrap `secret_key` in `config.py` to prevent "Fail to start" crashes if a secret is missing during deployment.

## 3. SQLAlchemy Async Requirements [IMPLEMENTED]
### Problem
Using a standard `postgresql://` string in an async engine results in a driver error. 
### Solution
- **Self-Healing**: We implemented a `field_validator` in `config.py` that automatically adds the **`+asyncpg`** driver prefix if it is missing from the environment string.

## 4. Neon SSL & Driver Compatibility [IMPLEMENTED]
### Problem
`asyncpg` does not recognize the standard Postgres `sslmode=require` and **`channel_binding=require`** parameters, causing the app to crash on startup.
### Solution
- **Self-Healing**: Our configuration validator now uses **Regex** to automatically:
    - Transform `sslmode=` to `ssl=`.
    - **Strip** incompatible `channel_binding` and `target_session_attrs` parameters entirety from the URL.
- This makes the backend "immune" to standard cloud connection string variations.

## 5. Debugging "Silent Crashes" in Cloud Run [IMPLEMENTED]
### Problem
If an app crashes during the import phase, Cloud Run reports a "TCP Probe Failed" without showing a traceback.
### Solution
- **Traceability**: We wrapped the early initialization in `main.py` with a `try/except` that prints **`❌ CRITICAL IMPORT ERROR`** to the terminal. This forces the error into the Cloud Run logs.

## 6. Local IDE vs. Docker Sync [COMPLETED]
### Problem
IDE showing "Module Not Found" despite the package being in `pyproject.toml`.
### Solution
- **Action**: Ran `uv sync` locally to update the `.venv` with `pydantic-settings`.
