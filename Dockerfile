# 1. First stage: Get uv binary from the official image
FROM ghcr.io/astral-sh/uv:latest AS uv_bin

# 2. Second stage: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy the uv executables from the first stage
COPY --from=uv_bin /uv /uvx /bin/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

# CRITICAL FIX: Cache mount for wheels
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# 3. Final execution stage (UPDATED TO 3.13)
FROM python:3.13-slim

WORKDIR /app

# Copy the pre-built virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy source code and dataset assets
COPY src/ /app/src/
COPY TrackMail_RAG_Dataset.docx /app/TrackMail_RAG_Dataset.docx

# Set path configurations
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]