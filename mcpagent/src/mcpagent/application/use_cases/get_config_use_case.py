from typing import Optional
from mcpagent.application.services.config import FastAPIConfig, OpenAIConfig, LangfuseConfig
from mcpagent.application.services.config.fastapi_config import FastAPIConfigModel, FastAPIConfig
from mcpagent.application.services.config.openai_config import OpenAIConfigModel, OpenAIConfigImpl
from mcpagent.application.services.config.langfuse_config import LangfuseConfigModel, LangfuseConfigImpl
from mcpagent.application.services.config.paths import get_env_file_path
from mcpagent.application.services.logger import LoggerInitializer


class GetConfigUseCase:
    """Use case for getting application configuration."""
    
    def __init__(self, env: str = "development"):
        """Initialize the use case.
        
        Args:
            env: The environment to load configuration for (e.g., 'development', 'testing', 'production').
        """
        self._env = env
        self._env_file = get_env_file_path(env)
        self._fastapi_config: Optional[FastAPIConfig] = None
        self._openai_config: Optional[OpenAIConfig] = None
        self._langfuse_config: Optional[LangfuseConfig] = None
        self._logger = None
    
    def get_fastapi_config(self) -> FastAPIConfig:
        """Get the FastAPI configuration.
        
        Returns:
            FastAPIConfig: The FastAPI configuration.
        """
        if self._fastapi_config is None:
            config_model = FastAPIConfigModel.from_env_file(self._env_file)
            self._fastapi_config = FastAPIConfig(config_model)
        return self._fastapi_config
    
    def get_openai_config(self) -> OpenAIConfig:
        """Get the OpenAI configuration.
        
        Returns:
            OpenAIConfig: The OpenAI configuration.
        """
        if self._openai_config is None:
            config_model = OpenAIConfigModel.from_env_file(self._env_file)
            self._openai_config = OpenAIConfigImpl(config_model)
        return self._openai_config
    
    def get_langfuse_config(self) -> LangfuseConfig:
        """Get the Langfuse configuration.
        
        Returns:
            LangfuseConfig: The Langfuse configuration.
        """
        if self._langfuse_config is None:
            config_model = LangfuseConfigModel.from_env_file(self._env_file)
            self._langfuse_config = LangfuseConfigImpl(config_model)
        return self._langfuse_config

    def get_logger(self):
        if self._logger is None:
            self._logger = LoggerInitializer.get_default_logger()
        return self._logger







