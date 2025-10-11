from pydantic import BaseModel

class EventEmailPayload(BaseModel):
    subject: str
    body: str
    user_id: str
    thread_id: str | None = None
    metadata: dict | None = None
