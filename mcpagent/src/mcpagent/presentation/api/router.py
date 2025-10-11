from fastapi import APIRouter, FastAPI
from .routes import events, response_ws


router = APIRouter()

# Include all route modules
router.include_router(events.router)
router.include_router(response_ws.router)
