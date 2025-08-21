from pydantic import BaseModel
from typing import List

class LLMConfig(BaseModel):
    """Configuration for the LLM."""
    model: str
    temperature: float = 0.7
    max_tokens: int = 1500
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] = []
    # Add other configuration fields as needed