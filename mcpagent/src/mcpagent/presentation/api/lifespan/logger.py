from fastapi import FastAPI
from mcpagent.infrastructure.logger import LoggerInitializer

async def init_logger(app: FastAPI):
    app.state.logger = LoggerInitializer.get_default_logger()
    app.state.logger.info(f"Logger initialized.")