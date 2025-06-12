import openai
from typing import List, Optional, Dict, Any, AsyncGenerator
from langchain_core.messages import BaseMessage, AIMessage

from mcpagent.domain.interfaces.llm import LLMInterface


class OpenAILLM(LLMInterface):
    """OpenAI implementation of the LLM interface."""
    
    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        api_key: Optional[str] = None,
        organization: Optional[str] = None
    ):
        """Initialize the OpenAI LLM.
        
        Args:
            model: The OpenAI model to use
            api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
            organization: OpenAI organization ID (if None, uses OPENAI_ORG_ID env var)
        """
        self.model = model
        self.client = openai.AsyncOpenAI(
            api_key=api_key,
            organization=organization
        )
    
    async def generate(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> BaseMessage:
        """Generate a response using OpenAI's API."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": msg.type, "content": msg.content} for msg in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            **kwargs
        )
        
        return AIMessage(content=response.choices[0].message.content)
    
    async def generate_stream(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> AsyncGenerator[BaseMessage, None]:
        """Generate a stream of responses using OpenAI's API."""
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": msg.type, "content": msg.content} for msg in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            stream=True,
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield AIMessage(content=chunk.choices[0].delta.content)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the OpenAI model being used."""
        return {
            "provider": "OpenAI",
            "model": self.model,
            "capabilities": {
                "streaming": True,
                "function_calling": True,
                "vision": "gpt-4-vision" in self.model
            }
        } 