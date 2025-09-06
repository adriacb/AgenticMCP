from mcpagent.src.mcpagent.presentation.api.app import app
from mcpagent.infrastructure.config.settings import load_settings

FASTAGENT_ENV = "dev"

if __name__ == "__main__":
    import uvicorn

    settings = load_settings(FASTAGENT_ENV)
    uvicorn.run(
            app, 
            host=settings.FASTAGENT_API_HOST, 
            port=settings.FASTAGENT_API_PORT, 
            reload=settings.FASTAGENT_API_RELOAD
        )
