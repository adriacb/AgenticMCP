from fastapi import FastAPI
from mcpagent.presentation.api.middleware import add_middleware
from mcpagent.presentation.api.routes import register_routes
from mcpagent.presentation.api.error_handling import add_exception_handlers

app = FastAPI(title="LangGraph API")

add_middleware(app)
add_exception_handlers(app)
register_routes(app) 