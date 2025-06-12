from typing import Dict, Optional, List
from pydantic import Field, BaseModel, field_validator
from .base import LangfuseConfig, BaseConfigModel

class LangfuseConfigModel(BaseConfigModel):
    """Pydantic model for Langfuse configuration."""
    public_key: str = Field(..., alias="LANGFUSE_PUBLIC_KEY")
    secret_key: str = Field(..., alias="LANGFUSE_SECRET_KEY")
    host: str = Field(default="https://cloud.langfuse.com", alias="LANGFUSE_HOST")
    timeout: Optional[int] = Field(default=None, alias="LANGFUSE_TIMEOUT")
    tags: List[str] = Field(..., alias="LANGFUSE_TAGS")
    version: str = Field(default="0.1.0", alias="LANGFUSE_VERSION")
    release: str = Field(default="development", alias="LANGFUSE_RELEASE")
    environment: str = Field(default="development", alias="LANGFUSE_ENVIRONMENT")

    @field_validator('tags', mode='before')
    def split_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(',') if tag.strip()]
        return v

class LangfuseConfigImpl(LangfuseConfig):
    """Langfuse configuration implementation."""
    
    def __init__(self, config: LangfuseConfigModel):
        """Initialize Langfuse configuration.
        
        Args:
            config: LangfuseConfigModel instance containing the configuration.
        """
        self._config = config
    
    def get_public_key(self) -> str:
        return self._config.public_key
    
    def get_secret_key(self) -> str:
        return self._config.secret_key
    
    def get_host(self) -> str:
        return self._config.host
    
    def get_timeout(self) -> Optional[int]:
        return self._config.timeout
    
    def get_tags(self) -> List[str]:
        return self._config.tags
    
    def get_version(self) -> str:
        return self._config.version
    
    def get_release(self) -> str:
        return self._config.release
    
    def get_environment(self) -> str:
        return self._config.environment 