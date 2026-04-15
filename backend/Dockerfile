# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies
# curl: Required for internal health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (blazing fast python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment configuration
# Ensure logs are flushed immediately for visibility
ENV PYTHONUNBUFFERED=1
# Force uv to install into global site-packages (resolves ModuleNotFoundError)
ENV UV_SYSTEM_PYTHON=1
# Default port for local/cloud flexibility
ENV PORT=8080

# Create a non-root user and prepare workspace
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser
WORKDIR /app
RUN chown appuser:appgroup /app

# Switch to non-root user for all subsequent operations
USER appuser

# Copy dependency files first to leverage build cache
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./

# Install dependencies into the system environment
# This is the "Magic Bullet" command from your successful project
# It ensures binaries like uvicorn are placed in /usr/local/bin
USER root
RUN uv pip install --system --no-cache -r pyproject.toml

# Switch back to non-root user
USER appuser

# Copy the actual backend code
COPY --chown=appuser:appgroup . .

# Expose backend port
EXPOSE 8080

# Start FastAPI via uvicorn
# We use shell form to allow native $PORT substitution from Cloud Run env
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
