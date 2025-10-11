from pydantic import BaseModel

class EventChatPayload(BaseModel):
    message: str
    user_id: str
    thread_id: str
