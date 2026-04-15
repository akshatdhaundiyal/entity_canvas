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

# # Create a non-root user and prepare workspace
# RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser
# WORKDIR /app
# RUN chown appuser:appgroup /app

# Switch to non-root user for all subsequent operations
# USER appuser

# Set working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies into the system environment to avoid virtualenv overhead in Docker
RUN uv pip install --system -r pyproject.toml

# Copy the actual backend code
COPY . .

# Create images directory (Git doesn't track empty folders)
RUN mkdir -p images

# Expose backend port (Cloud Run standard is 8080)
EXPOSE 8080

# Start FastAPI via uvicorn
# We use shell form to allow native $PORT substitution from Cloud Run env
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}