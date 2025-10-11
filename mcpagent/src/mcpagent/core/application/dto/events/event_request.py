from pydantic import BaseModel
from typing import Literal
from ..payloads import EventEmailPayload, EventChatPayload

class EventRequest(BaseModel):
    event_type: Literal["email", "chat"]
    payload: EventEmailPayload | EventChatPayload
    metadata: dict | None = None