from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncGenerator

from langchain_core.messages import BaseMessage


class LLMInterface(ABC):
    """Interface defining the contract for any LLM implementation.
    
    This interface abstracts away the specific LLM provider (OpenAI, Anthropic, etc.)
    and defines the core capabilities that any LLM must provide in our domain.
    """
    
    @abstractmethod
    async def generate(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> BaseMessage:
        """Generate a response based on the input messages.
        
        Args:
            messages: List of messages to generate a response for
            temperature: Controls randomness in the output
            max_tokens: Maximum number of tokens to generate
            stop: List of strings that stop generation when encountered
            **kwargs: Additional provider-specific parameters
            
        Returns:
            The generated message
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> AsyncGenerator[BaseMessage, None]:
        """Generate a stream of responses based on the input messages.
        
        Args:
            messages: List of messages to generate a response for
            temperature: Controls randomness in the output
            max_tokens: Maximum number of tokens to generate
            stop: List of strings that stop generation when encountered
            **kwargs: Additional provider-specific parameters
            
        Returns:
            An async generator yielding message chunks
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the LLM model being used.
        
        Returns:
            Dictionary containing model information (name, version, capabilities, etc.)
        """
        pass 