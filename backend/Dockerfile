FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies if needed (none for now)
# RUN apt-get update && apt-get install -y --no-install-recommends ... && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Ensure the virtual environment is used
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies using uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["python", "main.py"]
