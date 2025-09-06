## Multi-stage Dockerfile
## 1) Builder stage: install build deps and build a wheel
FROM python:3.12-slim AS builder
WORKDIR /app

# Install system build deps (kept minimal), build wheel and clean caches
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata and sources
COPY pyproject.toml setup.cfg ./
COPY mcpagent ./mcpagent

# Build a wheel into /wheels and cleanup build-time caches
RUN python -m pip install --upgrade pip build setuptools wheel \
    && python -m pip wheel . --wheel-dir /wheels \
    && python -m pip cache purge || true \
    && apt-get purge -y --auto-remove build-essential gcc || true \
    && rm -rf /var/lib/apt/lists/* /root/.cache/pip

## 2) Runtime stage: install the wheel and run
FROM python:3.12-slim AS runtime
WORKDIR /app

# Copy built wheels from builder and install them
COPY --from=builder /wheels /wheels
RUN python -m pip install --upgrade pip \
    && pip install /wheels/*.whl \
    && pip install uvicorn[standard] \
    && python -m pip cache purge || true

# Copy only the package source for convenience (not strictly required)
COPY mcpagent ./mcpagent

# Create a non-root user and take ownership of /app
RUN groupadd -g 1000 appuser || true \
    && useradd -u 1000 -g appuser -m -s /usr/sbin/nologin appuser || true \
    && chown -R appuser:appuser /app

# Switch to non-root
USER appuser

# Expose port for the ASGI server
EXPOSE 8000

# Run the application with uvicorn (ASGI)
CMD ["uvicorn", "mcpagent.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
