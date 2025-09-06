# How to: run, test and deploy

This page contains quick, copyable instructions for common developer workflows: running the API locally, building and running the Docker image, running tests and coverage, using `Makefile` targets, and a short note about CI/CD.

## Run the API (development)

The project uses an ASGI app at `mcpagent.presentation.api.app:app`. You can run it with `uvicorn` or the project's runner if configured.

PowerShell (recommended for Windows):

```powershell
# Install dev deps if needed
python -m pip install --upgrade pip
pip install -e .[dev]

# Run with uvicorn (dev)
uvicorn mcpagent.presentation.api.app:app --reload --host 0.0.0.0 --port 8000

# Alternative: if you use the repo runner 'uv' (project-specific),
# adjust to: uv run path\to\script.py
```

Open http://localhost:8000 in your browser (or the configured port).

## Build and run with Docker

The repository contains a multi-stage `Dockerfile` that builds a wheel and installs it in a slim runtime image. Example commands (PowerShell):

```powershell
# Build the image
docker build -t mcpagent:local .

# Run the container and map port 8000
docker run --rm -p 8000:8000 mcpagent:local

# Check logs
docker logs <container-id>

# To run in detached mode and name the container
docker run -d --name mcpagent_local -p 8000:8000 mcpagent:local
```

Quick usage (docker-compose):

```powershell
# Build and start via docker-compose (will build locally and not push to any registry)
docker compose up --build

# Start in background
docker compose up --build -d

# Stop and remove containers
docker compose down
```

Notes:
- The container runs `uvicorn mcpagent.presentation.api.app:app` by default. If your app's ASGI import path differs, change the `CMD` in the `Dockerfile`.
- To publish images from CI, add push steps to the workflow and store registry credentials as secrets.

## Tests and coverage

Run unit tests with pytest. Use `pytest-cov` to produce a coverage report.

PowerShell:

```powershell
# Run tests
pytest -q

# Run tests with coverage and write XML (for Codecov)
pytest -q --cov=mcpagent --cov-report=term --cov-report=xml:coverage.xml
```

Upload the resulting `coverage.xml` to your coverage provider (Codecov, Coveralls) or use the GitHub Actions workflow already included in `.github/workflows/ci.yaml`.

## Makefile targets

The project contains a `Makefile` under `mcpagent/Makefile` (edit or extend if needed). Common targets to add/use:

- `install` — install editable package and dev dependencies
- `lint` — run `ruff` or other linters
- `test` — run `pytest`
- `coverage` — run `pytest` with coverage and generate `coverage.xml`
- `docker-build` — build the project Docker image

Example usage (PowerShell):

```powershell
# From repo root
make -C mcpagent install
make -C mcpagent lint
make -C mcpagent test
make -C mcpagent coverage
make -C mcpagent docker-build
```

## CI/CD (GitHub Actions)

This repo contains a GitHub Actions workflow at `.github/workflows/ci.yaml` that runs linting, tests, coverage, and (optionally) builds the Docker image on pushes to `main`.

How it works:
- `lint-and-test` job runs on PRs and pushes to `development`/`main`: installs dependencies, runs `ruff`, runs `pytest` with coverage, uploads `coverage.xml` and sends it to Codecov.
- `build-and-push` job runs only on `push` to `main` and depends on `lint-and-test`. It builds a Docker image; add registry push steps (Docker Hub, GHCR, etc.) and configure secrets (e.g., `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) to enable publishing.

Quick checklist to enable publishing from CI:

1. In repository Secrets, add credentials for your container registry (e.g., `REGISTRY_USER`, `REGISTRY_TOKEN`) and for Codecov if you require it.
2. Update `.github/workflows/ci.yaml` to log in and push the built image. See Docker login actions or `docker/build-push-action` for multi-arch builds.

## Troubleshooting

- If the ASGI import path fails (`ModuleNotFoundError`), verify the package is installed and the path `mcpagent.presentation.api.app:app` is correct.
- If Docker build fails due to missing headers or build deps, ensure the `Dockerfile` builder stage includes required system packages for native extensions.
- If tests fail in CI but pass locally, confirm Python versions and installed extras match (the workflow uses Python 3.12).

## Want me to add more?

I can:
- Add a `docker-compose.yml` for local development with dependent services (databases, vector DB, etc.).
- Add a `Makefile` at repo root that proxies into `mcpagent/Makefile` for easier top-level commands.
- Add GitHub Actions steps to publish images to Docker Hub or GHCR (I will need the registry name and desired image tags).
