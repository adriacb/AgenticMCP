from mcpagent.application.services.config.base import BaseConfigModel
from pydantic import Field

class OpenAILLMConfig(BaseConfigModel):
    """Configuration for OpenAI LLM."""
    api_key: str = Field(..., alias="OPENAI_API_KEY")
    model: str = Field(..., alias="OPENAI_MODEL")
    temperature: float = Field(..., alias="OPENAI_TEMPERATURE")
    max_tokens: int = Field(..., alias="OPENAI_MAX_TOKENS")
    top_p: float = Field(..., alias="OPENAI_TOP_P")
    logprobs: int = Field(..., alias="OPENAI_LOGPROBS")

    def to_dict(self) -> dict:
        return self.model_dump()
