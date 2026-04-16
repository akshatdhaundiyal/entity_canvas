# Knowledge Base 05: Docker Development Patterns & Hot-Reload

This document outlines the architectural patterns used to create a "Live Coding" environment in Entity Canvas, where local file changes are instantly reflected inside Docker containers.

## 🔄 Pattern: The "Docker-Native" Dev Loop

Instead of adding development-specific logic to the application code (e.g., checking for `DEBUG` flags in `main.py`), we use the Docker orchestrator (`docker-compose.yml`) to transform the container at runtime.

### 1. Command Overrides
We keep the `Dockerfile` entry point clean for production but override it in development:
- **Production**: `CMD uvicorn main:app`
- **Development**: `command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]`
- **Learning**: This keeps the production container immutable while giving developers a "God Mode" reloader locally.

### 2. Multi-Stage Development Targets
We use a single `Dockerfile` with multiple stages and tell Docker where to stop in the `docker-compose.yml`:
```yaml
# docker-compose.yml
build:
  context: ./frontend
  target: development  # Stops build here for dev
```
- **Learning**: This allows sharing the `base` stage (shared dependencies) between dev and prod while ensuring the dev container runs `npm run dev` (HMR) and the prod container serves a optimized static bundle.

---

## 🛡️ Pattern: Dependency Shielding (Shadow Volumes)

One of the most common "Docker on Windows" failures is when a local `node_modules` or `.venv` folder overwrites the one inside the container.

### The Conflict
- **Host**: Windows filesystem, often missing dependencies or having Windows-specific binaries.
- **Container**: Linux filesystem, requiring specific ELF binaries.

### The Solution: Anonymous Volumes
By defining a volume for the dependency folder *without* a host mapping, we "shield" it:
```yaml
volumes:
  - ./frontend:/app           # Map source code (Visible to Host)
  - /app/node_modules          # "Shadow" volume (Isolated from Host)
```
- **Learning**: Docker will now prioritize the internal `/app/node_modules` over the one coming from your Windows machine, preventing `ModuleNotFoundError` or binary execution errors.

---

## 🏗️ Technical Hurdles: Windows File Events

### The Problem: Silent Saves
On Windows (WSL2/Hyper-V), file system events (inotify) often fail to propagate from the Windows host into the Linux container. This means you save a file, the file *changes* in the container, but the watcher (Vite/Nuxt/Uvicorn) doesn't "see" the event.

### The Fix: Polling
We force the watcher to manually check for changes using polling:
- **Frontend (Nuxt/Vite)**: `CHOKIDAR_USEPOLLING=true` and `WATCHPACK_POLLING=true`.
- **Backend (Uvicorn)**: Uvicorn's reload logic is generally more robust, but `--reload-dir` can be used if needed.

---

## ✅ Best Practices Checklist

1. **Keep App Code Pure**: Don't check `if ENV == 'dev'` in your Python/JS if you can handle it via `CMD` or `entrypoint`.
2. **Use .dockerignore**: Always ignore `node_modules`, `.venv`, and `__pycache__` to keep image builds fast and clean.
3. **Healthchecks**: Always add a healthcheck to the backend so the frontend waits for the API to be ready before starting.
