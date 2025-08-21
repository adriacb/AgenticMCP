from typing import List
from abc import ABC, abstractmethod
from .message_interface import BaseMessage

class AgentInterface(ABC):
    @abstractmethod
    def invoke(self, input: List[BaseMessage]) -> str:
        """Generate a response based on the input messages."""
        pass

    @abstractmethod
    async def ainvoke(self, input: List[BaseMessage]) -> str:
        """Asynchronously generate a response based on the input messages."""
        pass