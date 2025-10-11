from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from mcpagent.core.application.dto.payloads import EventChatPayload
from mcpagent.core.application.use_cases.handle_event_chat import HandleEventChat

router = APIRouter()

@router.websocket("/generate/stream")
async def generate_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    handler = HandleEventChat()
    app = websocket.app

    try:
        while True:
            data = await websocket.receive_json()
            event = EventChatPayload(**data)

            # Stream agent response
            stream = handler(
                graph=app.state.graph,
                event=event,
                callbacks=getattr(app.state, "callbacks", []),
            )

            async for chunk in stream:
                
                if 'call_model' in chunk:
                    await websocket.send_json({"event": "call_model", "call_model": chunk['call_model']['messages'][-1].content})
                

            # Signal end of stream
            await websocket.send_json({"event": "end_of_stream", "thread_id": event.thread_id})

    except WebSocketDisconnect:
        app.state.logger.info("Client disconnected from /generate/stream")
    except Exception as e:
        app.state.logger.error(f"Error in WebSocket stream: {e}")
        await websocket.close(code=1011, reason=str(e))
