from typing import Optional
from pydantic import Field
from .base import OpenAIConfig, BaseConfigModel

class OpenAIConfigModel(BaseConfigModel):
    """Pydantic model for OpenAI configuration."""
    api_key: str = Field(..., alias="OPENAI_API_KEY")
    model: str = Field(default="gpt-4", alias="OPENAI_MODEL")
    temperature: float = Field(default=0.7, alias="OPENAI_TEMPERATURE")
    max_tokens: Optional[int] = Field(default=None, alias="OPENAI_MAX_TOKENS")

class OpenAIConfigImpl(OpenAIConfig):
    """OpenAI configuration implementation."""
    
    def __init__(self, config: OpenAIConfigModel):
        """Initialize OpenAI configuration.
        
        Args:
            config: OpenAIConfigModel instance containing the configuration.
        """
        self._config = config
    
    def get_api_key(self) -> str:
        return self._config.api_key
    
    def get_model(self) -> str:
        return self._config.model
    
    def get_temperature(self) -> float:
        return self._config.temperature
    
    def get_max_tokens(self) -> Optional[int]:
        return self._config.max_tokens 