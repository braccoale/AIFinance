## Dockerfile for the AI Portfolio Orchestrator
##
## This image installs the necessary dependencies, copies the code and
## launches a Uvicorn server on port 8080.  It is intended for use
## with serverless container platforms such as Google Cloud Run or
## AWS App Runner.  Modify as needed for your environment.

FROM python:3.11-slim as base

# Install system dependencies (none needed beyond Python).  Update
# package indexes to ensure `pip` can fetch precompiled wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY orchestrator/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY orchestrator /app/orchestrator

# Expose port 8080 for Cloud Run/App Runner
EXPOSE 8080

# Set environment variables.  You can override these at runtime by
# passing `-e KEY=value` to docker run.  They can also be defined in
# a .env file on your host when using docker-compose.
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Default command: run Uvicorn server
CMD ["uvicorn", "orchestrator.main:app", "--host", "0.0.0.0", "--port", "8080"]