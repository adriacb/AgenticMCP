from pydantic import BaseModel


class AgentCard(BaseModel):
    """Represents a card for an agent with its configuration."""

    name: str = "Default Assistant"
    description: str = "A default assistant configuration."
    version: str = "1.0.0"
    system_prompt_key: str | None = "default"  # Literal
    skills: list[dict] = []
