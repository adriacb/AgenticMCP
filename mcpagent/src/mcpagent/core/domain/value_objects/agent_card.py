from pydantic import BaseModel

class AgentCard(BaseModel):
    """Represents a card for an agent with its configuration."""
    name: str="Default Assistant"
    description: str="A default assistant configuration."
    version: str="1.0.0"
    skills: list[dict] = []