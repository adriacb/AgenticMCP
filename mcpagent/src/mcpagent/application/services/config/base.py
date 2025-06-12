from abc import ABC, abstractmethod
from typing import Dict, Optional
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

class BaseConfigModel(BaseSettings):
    """Base configuration model with environment loading capabilities."""
    
    model_config = {
        "env_file": None,
        "env_file_encoding": "utf-8",
        "env_nested_delimiter": "__",
        "extra": "ignore",
        "populate_by_name": True,
        "validate_assignment": True,
        "env_prefix": "",
        "env_ignore_empty": True,
        "env_parse_file_values": True
    }
    
    @classmethod
    def from_env_file(cls, env_file: Optional[str | Path] = None) -> 'BaseConfigModel':
        """Create a configuration instance from an environment file.
        
        Args:
            env_file: Optional path to the environment file. If not provided, will look for .env in current directory.
            
        Returns:
            BaseConfigModel: Configuration instance with values loaded from environment.
        """
        if env_file:
            env_file = Path(env_file)
            if not env_file.exists():
                raise FileNotFoundError(f"Environment file not found: {env_file}")
            load_dotenv(env_file, override=True)
        
        return cls()

class APIConfig(ABC):
    """Base interface for API configuration."""
    
    @abstractmethod
    def get_host(self) -> str:
        """Get the host address."""
        pass

    @abstractmethod
    def get_port(self) -> int:
        """Get the port number."""
        pass

    @abstractmethod
    def get_workers(self) -> int:
        """Get the number of workers."""
        pass

    @abstractmethod
    def get_reload(self) -> bool:
        """Get whether to reload on changes."""
        pass

    @abstractmethod
    def get_access_log(self) -> bool:
        """Get whether to enable access logging."""
        pass

    @abstractmethod
    def get_api_prefix(self) -> str:
        """Get the API prefix."""
        pass

    @abstractmethod
    def get_api_title(self) -> str:
        """Get the API title."""
        pass

    @abstractmethod
    def get_api_description(self) -> str:
        """Get the API description."""
        pass

    @abstractmethod
    def get_api_version(self) -> str:
        """Get the API version."""
        pass

class OpenAIConfig(ABC):
    """Base interface for OpenAI configuration."""
    
    @abstractmethod
    def get_api_key(self) -> str:
        """Get the OpenAI API key."""
        pass

    @abstractmethod
    def get_model(self) -> str:
        """Get the OpenAI model name."""
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        """Get the temperature setting."""
        pass

    @abstractmethod
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum number of tokens."""
        pass

class LangfuseConfig(ABC):
    """Base interface for Langfuse configuration."""
    
    @abstractmethod
    def get_public_key(self) -> str:
        """Get the Langfuse public key."""
        pass

    @abstractmethod
    def get_secret_key(self) -> str:
        """Get the Langfuse secret key."""
        pass

    @abstractmethod
    def get_host(self) -> str:
        """Get the Langfuse host."""
        pass

    @abstractmethod
    def get_timeout(self) -> Optional[int]:
        """Get the timeout setting."""
        pass

    @abstractmethod
    def get_tags(self) -> Dict[str, str]:
        """Get the Langfuse tags."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get the Langfuse version."""
        pass

    @abstractmethod
    def get_release(self) -> str:
        """Get the Langfuse release."""
        pass

    @abstractmethod
    def get_environment(self) -> str:
        """Get the Langfuse environment."""
        pass 