from dataclasses import dataclass
from typing import Any


@dataclass
class ToolMessage:
    """Framework-agnostic message representing a tool's response."""
    role: str
    tool_call_id: str
    name: str
    content: Any

    def to_dict(self) -> dict:
        """Convert to a serializable dictionary (for LLM APIs)."""
        return {
            "role": self.role,
            "tool_call_id": self.tool_call_id,
            "name": self.name,
            "content": self.content,
        }
