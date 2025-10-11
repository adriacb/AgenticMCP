from fastapi import APIRouter, HTTPException, Request
from mcpagent.core.application.dto.events import EventRequest
from mcpagent.core.application.dto.payloads import EventEmailPayload, EventChatPayload

router = APIRouter()

@router.post("/events")
async def publish_event(request: Request, event: EventRequest):
    """
    Ingest external events (email, chat, etc.) and queue them for background processing.
    """
    if event.event_type == "email" and not isinstance(event.payload, EventEmailPayload):
        raise HTTPException(status_code=400, detail="Invalid payload for email event.")
    if event.event_type == "chat" and not isinstance(event.payload, EventChatPayload):
        raise HTTPException(status_code=400, detail="Invalid payload for chat event.")

    event_queue = request.app.state.event_queue  # ✅ correct way
    await event_queue.put(event.model_dump())

    return {"status": "queued"}
