from fastapi import APIRouter, WebSocket, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Any
from langchain_core.messages import HumanMessage


# from mcpagent.application.use_cases.langgraph import stream_response

router = APIRouter()


def register_routes(app: FastAPI):
    app.include_router(router)


class MessageRequest(BaseModel):
    user_id: str
    messages: List[Any]


@router.post("/generate/stream")
async def generate_stream_endpoint(request: MessageRequest):
    """Generate a response with streaming.

    Args:
        request: The request to generate a response for.

    Returns:
        A streaming response.
    """
    try:
        return StreamingResponse(
            # stream_response(
            #     graph=router.app.state.graph,
            #     query=request.messages,
            #     thread_id=request.user_id,
            #     callbacks=[router.app.state.langfuse_handler],
            #     ),
            # headers={"Content-Type": "text/event-stream"},
            # media_type="text/event-stream",
        )
    except Exception as e:
        app.state.logger.error(f"Error generating stream response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming responses."""

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            messages = [HumanMessage(content=msg) for msg in data.get("messages", [])]
            return messages
            # async for event in stream_response(messages):
            #     await websocket.send_json(event)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
