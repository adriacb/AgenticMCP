# Environment (.env) setup

This document describes the recommended .env layout and a small loader to pick `.env.dev` (default) or `.env.pro` (production) at startup.

## Files (project root)
- .env.dev — development defaults (checked into repo with non-sensitive placeholders)
- .env.pro — production secrets (not checked in; store in CI/secret manager)
- .env — optional fallback

Example .env.dev
```
OPENAI_API_KEY=dev-key-placeholder
LOG_LEVEL=DEBUG
APP_ENV=dev
```

Example .env.pro
```
OPENAI_API_KEY=sk-REPLACE_WITH_REAL_KEY
LOG_LEVEL=INFO
APP_ENV=pro
```

## How selection works
1. Read environment variable `APP_ENV` (if set).
2. If `APP_ENV == "pro"` -> load `.env.pro`.
3. Otherwise -> load `.env.dev`.
4. If the chosen file does not exist, fallback to `.env`, then system environment.

## Python loader (recommended)
- Add `python-dotenv` to your environment (pip install python-dotenv).
- Use this snippet at application entrypoint (e.g., in `mcpagent/__main__.py` or app bootstrap).

```python
# filepath: c:\Users\cabe\Documents\repos\agentic_summits\AgenticMCP\mcpagent\bootstrap_env.py
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]  # project root (adjust if needed)
app_env = os.environ.get("APP_ENV", "dev").lower()
candidate = ROOT / f".env.{app_env}"
fallback = ROOT / ".env"

if candidate.exists():
    load_dotenv(candidate)
elif fallback.exists():
    load_dotenv(fallback)
# environment variables from the OS remain available and override files
```

## Using settings in code
Option A — simple: use os.getenv
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

Option B — typed settings with pydantic BaseSettings (optional)
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"  # loader above already populated os.environ

settings = Settings()
```

## Running locally / CI
- Local (Windows PowerShell):
  - $env:APP_ENV="dev"; python -m mcpagent
- Local (Windows cmd):
  - set APP_ENV=pro && python -m mcpagent
- CI:
  - Set `APP_ENV=pro` and set secrets as CI environment variables or mount `.env.pro`.

## Tests
- Unit tests should not require real secrets. Either:
  - Monkeypatch env values in tests (monkeypatch.setenv("OPENAI_API_KEY", "test"))
  - Or mock external clients so no network call occurs.
- Example in pytest:
```python
def test_something(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    # run code that reads os.getenv("OPENAI_API_KEY")
```

## Notes / Best practices
- Keep `.env.pro` out of VCS. Add to `.gitignore`.
- `.env.dev` can be committed with non-sensitive placeholders.
- Prefer secret managers for production; use `.env.pro` only when necessary for deployment.