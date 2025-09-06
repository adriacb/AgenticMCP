from fastapi import FastAPI
from contextlib import asynccontextmanager

from mcpagent.presentation.api.middleware import add_middleware
from mcpagent.presentation.api.routes import register_routes
from mcpagent.presentation.api.error_handling import add_exception_handlers

from mcpagent.infrastructure.logger import LoggerInitializer

# from mcpagent.application.use_cases.langgraph import build_graph
# from mcpagent.application.services.logger import LoggerInitializer
# from mcpagent.application.services.monitoring.langfuse import get_langfuse_callback
# from mcpagent.application.services.config.langfuse_config import LangfuseConfig
# from mcpagent.infrastructure.memory import InMemorySaver

@asynccontextmanager
async def lifespan(app: FastAPI):
    # checkpointer = await get_mongodb_checkpointer(
    #     connection_string=settings.MONGO_URI,
    #     database_name=settings.MONGO_DB_NAME,
    #     collection_name="checkpoints",
    #     write_collection_name="checkpoints",
    #     )
    app.state.logger = LoggerInitializer.get_default_logger()
    #checkpointer = InMemorySaver()
    app.state.logger.info("Building LangGraph at startup...")
    yield   # 👈 this was missing!
    # app.state.graph = build_graph(checkpointer=checkpointer)  # or await if async
    # logger.info("LangGraph initialized.")
    # logger.info(f"Langfuse handler: {app.state.langfuse_handler}")
    # app.state.langfuse_handler = get_langfuse_callback(settings)
    # logger.info(f"Langfuse initialized.")
    # yield
    # logger.info("Shutting down...")  # optional cleanup


app = FastAPI(
    title="LangGraph API", 
    lifespan=lifespan
    )

add_middleware(app)
add_exception_handlers(app)
register_routes(app) 