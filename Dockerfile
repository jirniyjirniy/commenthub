# Syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Install system dependencies including postgresql-client for pg_isready
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files to the correct location
COPY backend/pyproject.toml /app/backend/

# Install dependencies
RUN cd /app/backend && uv pip install --no-cache -r pyproject.toml

# Copy backend code
COPY backend/ /app/backend/

# Copy entrypoint script
COPY entrypoint.sh /app/

# Create non-root user and directories
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/backend/staticfiles /app/backend/media && \
    chown -R appuser:appuser /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

USER appuser

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
