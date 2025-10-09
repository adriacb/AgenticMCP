from mcpagent.src.mcpagent.presentation.api.app import app
from mcpagent.infrastructure.config.settings import load_settings
import argparse

FASTAGENT_ENV = "dev"

if __name__ == "__main__":
    import uvicorn

    settings = load_settings(FASTAGENT_ENV)
    
    parser = argparse.ArgumentParser(description="Run the MCP Agent API server")
    parser.add_argument("--host", default=settings.FASTAGENT_API_HOST, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.FASTAGENT_API_PORT, help="Port to bind to")
    args = parser.parse_args()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=settings.FASTAGENT_API_RELOAD,
    )
