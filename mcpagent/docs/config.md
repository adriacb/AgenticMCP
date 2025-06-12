# Configuration System

The configuration system provides a clean and type-safe way to manage application settings using environment variables. It uses Pydantic for validation and type checking.

## Usage

### Basic Usage

```python
from mcpagent.application.use_cases.get_config_use_case import GetConfigUseCase

# Initialize with environment (defaults to "development")
config_use_case = GetConfigUseCase(env="development")

# Get configurations
fastapi_config = config_use_case.get_fastapi_config()
openai_config = config_use_case.get_openai_config()
langfuse_config = config_use_case.get_langfuse_config()

# Use the configurations
host = fastapi_config.get_host()
api_key = openai_config.get_api_key()
```

### Environment Files

Configuration is loaded from environment files located in `mcpagent/config/`:
- `.env.development` - Development environment
- `.env.testing` - Testing environment
- `.env.production` - Production environment

Example `.env.development`:
```env
# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_WORKERS=1
FASTAPI_RELOAD=true
FASTAPI_ACCESS_LOG=true
FASTAPI_API_PREFIX=/api
FASTAPI_API_TITLE=MCP Agent API
FASTAPI_API_DESCRIPTION=API for MCP Agent
FASTAPI_API_VERSION=0.1.0

# OpenAI Configuration
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_TIMEOUT=30
LANGFUSE_TAGS=["environment", "development"]
LANGFUSE_VERSION=0.1.0
LANGFUSE_RELEASE=development
LANGFUSE_ENVIRONMENT=development
```

## Adding a New Configuration

To add a new configuration (e.g., Anthropic), follow these steps:

1. **Create the Configuration Interface**

Create `mcpagent/src/mcpagent/application/services/config/anthropic_config.py`:
```python
from abc import ABC, abstractmethod
from typing import Optional

class AnthropicConfig(ABC):
    """Base interface for Anthropic configuration."""
    
    @abstractmethod
    def get_api_key(self) -> str:
        """Get the Anthropic API key."""
        pass

    @abstractmethod
    def get_model(self) -> str:
        """Get the Anthropic model name."""
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        """Get the temperature setting."""
        pass

    @abstractmethod
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum number of tokens."""
        pass
```

2. **Create the Pydantic Model**

Add to the same file:
```python
from pydantic import Field
from .base import BaseConfigModel

class AnthropicConfigModel(BaseConfigModel):
    """Pydantic model for Anthropic configuration."""
    api_key: str = Field(..., alias="ANTHROPIC_API_KEY")
    model: str = Field(default="claude-3-opus-20240229", alias="ANTHROPIC_MODEL")
    temperature: float = Field(default=0.7, alias="ANTHROPIC_TEMPERATURE")
    max_tokens: Optional[int] = Field(default=None, alias="ANTHROPIC_MAX_TOKENS")

class AnthropicConfigImpl(AnthropicConfig):
    """Anthropic configuration implementation."""
    
    def __init__(self, config: AnthropicConfigModel):
        self._config = config
    
    def get_api_key(self) -> str:
        return self._config.api_key
    
    def get_model(self) -> str:
        return self._config.model
    
    def get_temperature(self) -> float:
        return self._config.temperature
    
    def get_max_tokens(self) -> Optional[int]:
        return self._config.max_tokens
```

3. **Update the GetConfigUseCase**

Add to `mcpagent/src/mcpagent/application/use_cases/get_config_use_case.py`:
```python
from mcpagent.application.services.config.anthropic_config import (
    AnthropicConfig,
    AnthropicConfigModel,
    AnthropicConfigImpl
)

class GetConfigUseCase:
    def __init__(self, env: str = "development"):
        # ... existing init code ...
        self._anthropic_config: Optional[AnthropicConfig] = None
    
    def get_anthropic_config(self) -> AnthropicConfig:
        """Get the Anthropic configuration."""
        if self._anthropic_config is None:
            config_model = AnthropicConfigModel.from_env_file(self._env_file)
            self._anthropic_config = AnthropicConfigImpl(config_model)
        return self._anthropic_config
```

4. **Add Environment Variables**

Add to your `.env` files:
```env
# Anthropic Configuration
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_MODEL=claude-3-opus-20240229
ANTHROPIC_TEMPERATURE=0.7
ANTHROPIC_MAX_TOKENS=1000
```

5. **Add Tests**

Create tests in `tests/test_config.py`:
```python
def test_anthropic_config_loading():
    """Test loading Anthropic configuration."""
    config_model = AnthropicConfigModel.from_env_file(get_env_file_path("testing"))
    config = AnthropicConfigImpl(config_model)
    
    assert config.get_api_key() == "test-api-key"
    assert config.get_model() == "claude-3-opus-20240229"
    assert config.get_temperature() == 0.7
    assert config.get_max_tokens() == 1000
```

## Best Practices

1. **Type Safety**: Always use type hints and Pydantic models for configuration.
2. **Environment Variables**: Use uppercase with underscores for environment variable names.
3. **Default Values**: Provide sensible defaults in the Pydantic models.
4. **Documentation**: Document all configuration options in the code and README.
5. **Testing**: Write tests for all configuration models and implementations.
6. **Validation**: Use Pydantic's validation features to ensure configuration values are correct.
7. **Caching**: The configuration system caches loaded configurations for better performance. 