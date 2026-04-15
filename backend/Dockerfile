FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment configuration
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create a non-root user and prepare workspace
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser
WORKDIR /app
RUN chown appuser:appgroup /app

# Ensure uv has a writable cache within the app directory
ENV UV_CACHE_DIR="/app/.uv_cache"

# Switch to non-root user for all subsequent operations
USER appuser

# Install dependencies
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY --chown=appuser:appgroup . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
