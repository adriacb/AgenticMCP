from abc import ABC, abstractmethod


class LLMInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response based on the provided messages."""
        pass

    @abstractmethod
    async def agenerate(self, prompt: str) -> str:
        """Asynchronously generate a response based on the provided messages."""
        pass

    @abstractmethod
    def invoke(self, messages: list) -> str:
        """Invoke the LLM with the provided messages and return the response."""
        pass

    @abstractmethod
    async def ainvoke(self, messages: list) -> str:
        """Asynchronously invoke the LLM with the provided messages and return the response."""
        pass
