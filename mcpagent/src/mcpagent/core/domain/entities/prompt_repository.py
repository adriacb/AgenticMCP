from typing import Optional, Dict

from mcpagent.infrastructure.logger import LoggerInitializer
from mcpagent.core.domain.interfaces import PromptRegistryInterface
from mcpagent.core.domain.entities.prompts import (
    REACT_PROMPT,
    RETRIEVAL_QA_CHAT_PROMPT,
    REACT_JSON_PROMPT,
)

logger = LoggerInitializer.get_default_logger()


class InMemoryPromptRepository(PromptRegistryInterface):
    """
    Repository for managing prompts in memory.
    Provides CRUD operations with lazy initialization.
    """

    def __init__(self, registry: Optional[Dict[str, str]] = None) -> None:
        self._registry: Optional[Dict[str, str]] = registry

    @property
    def registry(self) -> Dict[str, str]:
        """Ensure registry is initialized before use."""
        if self._registry is None:
            self.compile()
        return self._registry

    def get_prompt(self, prompt_id: str) -> str:
        """Retrieve a prompt by its ID. Returns empty string if not found."""
        try:
            return self.registry.get(prompt_id, "")
        except Exception as e:
            logger.exception(f"Error getting prompt '{prompt_id}'")
            raise

    def add_prompt(self, prompt_id: str, prompt: str) -> str:
        """Create a new prompt. Overwrites if ID already exists."""
        try:
            self.registry[prompt_id] = prompt
            return prompt_id
        except Exception as e:
            logger.exception(f"Error creating prompt '{prompt_id}'")
            raise

    def update_prompt(self, prompt_id: str, prompt: str) -> str:
        """Update an existing prompt. Raises KeyError if not found."""
        try:
            if prompt_id not in self.registry:
                raise KeyError(f"Prompt '{prompt_id}' does not exist.")
            self.registry[prompt_id] = prompt
            return prompt_id
        except Exception as e:
            logger.exception(f"Error updating prompt '{prompt_id}'.", e)
            raise

    def remove_prompt(self, prompt_id: str) -> None:
        """Remove a prompt by its ID. Raises KeyError if not found."""
        try:
            del self.registry[prompt_id]
        except KeyError as e:
            logger.exception(f"Error removing prompt '{prompt_id}'.", e)
            raise

    def list_prompts(self):
        return f"Prompts: {list(self.registry.keys())}"

    def compile(self, registry: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Initialize or reinitialize the registry.
        If `registry` is provided, it will replace the current one.
        """
        try:
            if registry is not None:
                self._registry = registry
            else:
                self._registry = {
                    "default": "You are a helpful assistant.",
                    "react": REACT_PROMPT,
                    "retrieval_qa": RETRIEVAL_QA_CHAT_PROMPT,
                    "react_json": REACT_JSON_PROMPT,
                }
            return self._registry
        except Exception as e:
            logger.exception("Error compiling prompt registry.", e)
            raise
