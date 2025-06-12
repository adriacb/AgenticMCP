from abc import ABC, abstractmethod
from typing import List, AsyncGenerator, Dict, Union


class LLMInterface(ABC):
    """Interface for LLM clients.
    
    This interface defines the contract for both synchronous and asynchronous LLM clients.
    Implementations should provide either synchronous or asynchronous methods, but not both.
    """
    
    @abstractmethod
    def generate(self, prompt: str, instructions: str = "") -> str:
        """Generate a response for a prompt using the responses API.
        
        Args:
            prompt: The input prompt to generate a response for.
            instructions: Optional instructions to guide the response generation.
            
        Returns:
            The generated response as a string.
        """
        pass

    @abstractmethod
    async def agenerate(self, prompt: str, instructions: str = "") -> AsyncGenerator[str, None]:
        """Asynchronously generate a response for a prompt using the responses API.
        
        Args:
            prompt: The input prompt to generate a response for.
            instructions: Optional instructions to guide the response generation.
            
        Yields:
            Chunks of the generated response as they become available.
        """
        pass

    @abstractmethod
    def invoke(self, prompt: Union[str, List[Dict[str, str]]], stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        """Invoke the model with a prompt or message list.
        
        Args:
            prompt: Either a string prompt or a list of message dictionaries.
            stream: Whether to stream the response.
            
        Returns:
            If stream is False, returns the complete response as a string.
            If stream is True, returns an async generator that yields response chunks.
        """
        pass

    @abstractmethod
    async def ainvoke(self, prompt: Union[str, List[Dict[str, str]]], stream: bool = True) -> AsyncGenerator[str, None]:
        """Asynchronously invoke the model with a prompt or message list.
        
        Args:
            prompt: Either a string prompt or a list of message dictionaries.
            stream: Whether to stream the response (defaults to True for async).
            
        Yields:
            Chunks of the generated response as they become available.
        """
        pass