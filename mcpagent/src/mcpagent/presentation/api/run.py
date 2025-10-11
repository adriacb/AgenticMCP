from mcpagent.presentation.api.app import app
from mcpagent.infrastructure.config.settings import load_settings
import argparse
import os 

ENV_PATH = os.getenv("ENV_PATH", r"C:\Users\cabe\Documents\repos\agentic_summits\AgenticMCP\mcpagent\config\.env.pro")

if __name__ == "__main__":
    import uvicorn

    settings = load_settings(ENV_PATH)
    parser = argparse.ArgumentParser(description="Run the MCP Agent API server")
    parser.add_argument("--host", default=settings.fastapi.host, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.fastapi.port, help="Port to bind to")
    args = parser.parse_args()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=False,  # Disable reload when running file directly
    )
