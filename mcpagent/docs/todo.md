# Implementation TODO: CI/CD, Docker, Tests, Linting

This TODO lists the minimal steps and example snippets to add CI/CD, a Dockerfile, test coverage reporting, and linting with `ruff` for the `mcpagent` package.

Checklist
- [ ] CI/CD pipeline (GitHub Actions or equivalent)
- [ ] Dockerfile (container image for runtime)
- [x] Makefile present in repo — add standard targets if missing
- [ ] Test coverage reporting (pytest-cov + upload)
- [ ] Ruff / linting integrated into workflow

Guidance and examples

1) CI/CD (GitHub Actions — `.github/workflows/ci.yaml`)

Minimal set of jobs:
- install deps
- run linter (`ruff`)
- run tests + coverage
- (optional) build docker image and push

Example job snippet (place under `.github/workflows/ci.yaml`):

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest pytest-cov
      - name: Lint
        run: ruff check .
      - name: Test
        run: pytest -q --maxfail=1 --cov=mcpagent --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

2) Dockerfile (simple runtime image)

Place a `Dockerfile` at the repo root. Minimal example:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY mcpagent ./mcpagent
RUN python -m pip install --upgrade pip && pip install .
CMD ["python", "-m", "mcpagent.presentation.api.run"]
```

Adjust the `CMD` to the actual runtime entrypoint (for the demo runner you use `uv run` or the module that launches the app).

3) Makefile targets (extend existing `Makefile`)

If you already have a `Makefile`, add targets like below. Example content to add:

```makefile
.PHONY: install lint test coverage docker-build
install:
	python -m pip install --upgrade pip
	pip install -e .[dev]

lint:
	ruff check mcpagent

test:
	pytest -q

coverage:
	pytest -q --cov=mcpagent --cov-report=term --cov-report=xml:coverage.xml

docker-build:
	docker build -t myorg/mcpagent:latest .
```

4) Test coverage

- Add `pytest-cov` to dev dependencies.
- Use `--cov=mcpagent --cov-report=xml:coverage.xml` in CI to produce coverage reports and upload to Codecov or Coveralls.

Local command (PowerShell):

```powershell
# run tests with coverage
pytest -q --cov=mcpagent --cov-report=term --cov-report=xml:coverage.xml
```

5) Ruff / linting

- Add `ruff` as a dev dependency and configure it in `pyproject.toml` under `[tool.ruff]`.
- Basic local command:

```powershell
r For Windows PowerShell: ruff check .
```

Recommended `pyproject.toml` snippet for ruff:

```toml
[tool.ruff]
line-length = 88
extend-select = ["E", "F", "W"]
exclude = [".venv", "build", "dist"]
```

Notes and next steps
- Decide CI provider (GitHub Actions recommended for this repo).
- Pin python and dependency versions in CI for reproducibility.
- Consider adding `pre-commit` hooks for ruff/black/isort to keep code clean locally.
- Add a status badge to `README.md` after the pipeline is green.

If you want, I can implement the CI workflow YAML and the Dockerfile as a follow-up change and wire the Makefile targets into the repo; tell me which CI provider you prefer (GitHub Actions, Azure Pipelines, GitLab CI, etc.).
