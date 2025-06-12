from abc import ABC, abstractmethod

class PromptRepository(ABC):
    @abstractmethod
    def get_prompt(self, prompt_id: str) -> str:
        pass

    @abstractmethod
    def create_prompt(self, prompt: str) -> str:
        pass

    @abstractmethod
    def update_prompt(self, prompt_id: str, prompt: str) -> str:
        pass
    
    @abstractmethod
    def compile(self, **kwargs) -> str:
        pass