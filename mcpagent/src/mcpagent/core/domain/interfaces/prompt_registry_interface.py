from abc import ABC, abstractmethod

class PromptRegistryInterface(ABC):
    @abstractmethod
    def get_prompt(self, prompt_id: str) -> str:
        """Retrieve a prompt by its name."""
        pass

    @abstractmethod
    def add_prompt(self, prompt_id: str, prompt_content: str) -> None:
        """Add a new prompt to the registry."""
        pass

    @abstractmethod
    def remove_prompt(self, prompt_id: str) -> None:
        """Remove a prompt from the registry."""
        pass

    @abstractmethod
    def list_prompts(self) -> list:
        """List all available prompts."""
        pass