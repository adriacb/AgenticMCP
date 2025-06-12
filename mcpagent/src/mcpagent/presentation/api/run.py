import os
from mcpagent.presentation.api.app import app
from mcpagent.application.use_cases import GetConfigUseCase


config = GetConfigUseCase(env="development")


if __name__ == "__main__":
    import uvicorn

    if os.getenv("FASTAGENT_ENV") == "development":
        uvicorn.run(app, host=os.getenv("FASTAGENT_API_HOST"), port=os.getenv("FASTAGENT_API_PORT"))
    else:
        uvicorn.run(app, host=os.getenv("FASTAGENT_API_HOST"), port=os.getenv("FASTAGENT_API_PORT"), reload=False)
