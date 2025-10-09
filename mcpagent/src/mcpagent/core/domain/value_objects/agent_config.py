from pydantic import BaseModel
from typing import List, Any, Union
from .llm_config import LLMConfig
from .agent_card import AgentCard


class AgentConfig(BaseModel):
    llm_config: LLMConfig
    agent_card: AgentCard = AgentCard()
    system_prompt: str = "You are a helpful assistant."
