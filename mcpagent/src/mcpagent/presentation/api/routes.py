from fastapi import APIRouter, WebSocket, FastAPI
from pydantic import BaseModel
from typing import List, Any
from langchain_core.messages import HumanMessage

from mcpagent.application.langgraph_use_cases import generate_response, generate_stream

router = APIRouter()

class MessageRequest(BaseModel):
    messages: List[Any]

@router.post("/generate")
async def generate(request: MessageRequest):
    """Generate a response without streaming."""
    return await generate_response(request.messages)

@router.post("/generate/stream")
async def generate_stream_endpoint(request: MessageRequest):
    """Generate a response with streaming."""
    return generate_stream(request.messages)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming responses."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            messages = [HumanMessage(content=msg) for msg in data.get("messages", [])]
            async for event in generate_stream(messages):
                await websocket.send_json(event)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()

def register_routes(app: FastAPI):
    app.include_router(router) 