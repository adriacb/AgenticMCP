from langfuse import Langfuse

from mcpagent.application.services.config.langfuse_config import LangfuseConfig
from mcpagent.application.services.logger import LoggerInitializer
from mcpagent.domain.interfaces.prompt_repository import PromptRepository

logger = LoggerInitializer.get_default_logger()


class LangfusePromptRepository(PromptRegistry):
    def __init__(self, config: LangfuseConfig):
        try:
            self.langfuse = Langfuse(
                public_key=config.langfuse_public_key,
                secret_key=config.langfuse_secret_key,
                host=config.langfuse_host,
                timeout=config.langfuse_timeout,
                tags=config.langfuse_tags,
            )
        except Exception as e:
            logger.error(f"Error initializing Langfuse: {e}")
            raise e

    def get_prompt(self, prompt_id: str) -> str:
        try:
            return self.langfuse.get_prompt(prompt_id)
        except Exception as e:
            logger.error(f"Error getting prompt: {e}")
            raise e
    
    def create_prompt(self, prompt: str) -> str:
        try:
            return self.langfuse.create_prompt(prompt)
        except Exception as e:
            logger.error(f"Error creating prompt: {e}")
            raise e
    
    def update_prompt(self, prompt_id: str, prompt: str) -> str:
        """Update a prompt in Langfuse.
        
        Note: Langfuse does not support updating prompts directly.
        This method is implemented to satisfy the interface but will raise NotImplementedError.
        """
        raise NotImplementedError("Langfuse does not support updating prompts directly")
    
    def compile(self, **kwargs) -> str:
        try:
            return self.langfuse.compile(**kwargs)
        except Exception as e:
            logger.error(f"Error compiling prompt: {e}")
            raise e
