from abc import ABC, abstractmethod
from typing import Any, List, AsyncGenerator


class AgentInterface(ABC):
    """Base agent class that defines the core agent behavior.
    """
    
    @abstractmethod
    async def ainvoke(self, messages: List[Any]) -> Any:
        """Invoke the agent with a list of messages."""
        pass

    @abstractmethod
    async def astream(self, messages: List[Any]) -> AsyncGenerator[Any, None]:
        """Stream the agent's response to the client."""
        pass
