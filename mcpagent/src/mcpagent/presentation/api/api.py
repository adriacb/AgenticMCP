from fastapi import FastAPI
from contextlib import asynccontextmanager
from mcpagent.presentation.api.middleware import add_middleware
from mcpagent.presentation.api.routes import register_routes
from mcpagent.presentation.api.error_handling import add_exception_handlers
from mcpagent.application.services.logger import LoggerInitializer
from mcpagent.application.services.monitoring.langfuse import get_langfuse_callback
from mcpagent.application.services.config.langfuse_config import LangfuseConfig

logger = LoggerInitializer.get_default_logger()
settings = LangfuseConfig()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Building LangGraph at startup...")
    app.state.graph = build_graph()  # or await if async
    logger.info("LangGraph initialized.")
    logger.info(f"Langfuse handler: {app.state.langfuse_handler}")
    app.state.langfuse_handler = get_langfuse_callback(settings)
    logger.info(f"Langfuse initialized.")
    yield
    logger.info("Shutting down...")  # optional cleanup


app = FastAPI(
    title="LangGraph API", 
    lifespan=lifespan
    )

add_middleware(app)
add_exception_handlers(app)
register_routes(app) 