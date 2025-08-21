from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from mcpagent.core.domain.interfaces import BaseMessage

class ChatAgentInput(BaseModel):
    messages: List[BaseMessage]
    # Add other fields as needed, e.g. messages, tools, etc.

class ChatAgentOutput(BaseModel):
    response: str
    metadata: Optional[Dict[str, Any]] = None