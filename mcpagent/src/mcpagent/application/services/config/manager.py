from typing import Optional, Dict, Type, TypeVar
from pathlib import Path
from .base import BaseConfigModel
from .fastapi_config import FastAPIConfigModel, FastAPIConfig
from .openai_config import OpenAIConfigModel, OpenAIConfigImpl
from .langfuse_config import LangfuseConfigModel, LangfuseConfigImpl
from .paths import get_env_file_path, get_default_env_file_path
from dotenv import load_dotenv

T = TypeVar('T', bound=BaseConfigModel)

class ConfigManager:
    """Manages both general and service-specific configurations."""
    
    def __init__(self, env: str = "development", env_file: Optional[str | Path] = None):
        """Initialize the configuration manager.
        
        Args:
            env: The environment name (e.g., 'development', 'production', 'testing').
            env_file: Optional path to the environment file. If not provided, will use the default path for the environment.
        """
        if env_file is None:
            env_file = get_env_file_path(env)
            if not env_file.exists():
                env_file = get_default_env_file_path()
        
        self._env_file = env_file
        self._configs: Dict[Type[BaseConfigModel], BaseConfigModel] = {}
    
    def get_config(self, config_type: Type[T]) -> T:
        """Get a configuration instance of the specified type.
        
        Args:
            config_type: The type of configuration to get.
            
        Returns:
            T: The configuration instance.
            
        Raises:
            ValueError: If the configuration type is not supported.
        """
        if config_type not in self._configs:
            if config_type == FastAPIConfigModel:
                self._configs[config_type] = FastAPIConfigModel.from_env_file(self._env_file)
            elif config_type == OpenAIConfigModel:
                self._configs[config_type] = OpenAIConfigModel.from_env_file(self._env_file)
            elif config_type == LangfuseConfigModel:
                self._configs[config_type] = LangfuseConfigModel.from_env_file(self._env_file)
            else:
                raise ValueError(f"Unsupported configuration type: {config_type}")
        
        return self._configs[config_type]
    
    def get_fastapi_config(self) -> FastAPIConfig:
        """Get the FastAPI configuration.
        
        Returns:
            FastAPIConfig: The FastAPI configuration instance.
        """
        config = self.get_config(FastAPIConfigModel)
        return FastAPIConfig(config)
    
    def get_openai_config(self) -> OpenAIConfigImpl:
        """Get the OpenAI configuration.
        
        Returns:
            OpenAIConfigImpl: The OpenAI configuration instance.
        """
        config = self.get_config(OpenAIConfigModel)
        return OpenAIConfigImpl(config)
    
    def get_langfuse_config(self) -> LangfuseConfigImpl:
        """Get the Langfuse configuration.
        
        Returns:
            LangfuseConfigImpl: The Langfuse configuration instance.
        """
        config = self.get_config(LangfuseConfigModel)
        return LangfuseConfigImpl(config) 