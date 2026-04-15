# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install uv (blazing fast python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment configuration
# Ensure logs are flushed immediately for visibility
ENV PYTHONUNBUFFERED=1
# Set the port variable for local testing fallback
ENV PORT=8080

# Create a non-root user for security
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies into the system environment
# This avoids virtualenv overhead and permission issues in containerized environments
RUN uv sync --system --no-dev --no-install-project

# Copy the actual backend code
COPY . .

# Set ownership for any potential runtime file generation
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose backend port
EXPOSE 8080

# Start FastAPI via uvicorn
# We use shell form to allow native $PORT substitution from Cloud Run
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
