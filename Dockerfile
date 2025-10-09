# --------------------------
# 1) Builder stage
# --------------------------
    FROM python:3.12-slim AS builder
    WORKDIR /app
    
    # Install uv and build tools
    RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential gcc \
        && pip install uv \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy project metadata and sources
    COPY mcpagent/pyproject.toml ./mcpagent/
    COPY mcpagent/README.md ./mcpagent/
    COPY mcpagent/src ./mcpagent/src
    
    # Install dependencies and package in editable mode
    WORKDIR /app/mcpagent
    RUN uv sync
    RUN uv run pip install -e .
    
    # --------------------------
    # 2) Runtime stage
    # --------------------------
    FROM python:3.12-slim AS runtime
    WORKDIR /app
    
    # Install uv (needed to run)
    RUN pip install uv
    
    # Copy installed packages and binaries from builder
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    COPY --from=builder /usr/local/bin /usr/local/bin
    
    # Copy the source code
    COPY mcpagent/src /app/mcpagent/src
    
    # Set PYTHONPATH to include the source directory
    ENV PYTHONPATH=/app/mcpagent/src
    
    # Create non-root user
    RUN groupadd -g 1000 appuser || true \
        && useradd -u 1000 -g appuser -m -s /usr/sbin/nologin appuser \
        && chown -R appuser:appuser /app
    USER appuser
    
    EXPOSE 8000
    
    CMD ["uv", "run", "uvicorn", "mcpagent.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
    