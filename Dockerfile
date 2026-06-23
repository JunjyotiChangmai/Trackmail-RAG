# 1. First stage: Get uv binary from the official image
FROM ghcr.io/astral-sh/uv:latest AS uv_bin

# 2. Second stage: Build dependencies inside a standard python-slim image
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy the uv executables from the first stage
COPY --from=uv_bin /uv /uvx /bin/

# Enable bytecode compilation and extend network timeouts for heavy downloads
ENV UV_COMPILE_BYTECODE=1
ENV UV_HTTP_TIMEOUT=300

# Copy dependency files
COPY pyproject.toml uv.lock ./

# CRITICAL FIX: Use BuildKit caching so successfully downloaded wheels are NEVER lost between failed retries
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# 3. Final execution stage
FROM python:3.12-slim

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