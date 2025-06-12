from typing import Any, AsyncGenerator, List
from abc import ABC, abstractmethod

class AgentInterface(ABC):
    @abstractmethod
    async def ainvoke(self, messages: List[Any]) -> Any:
        pass

    @abstractmethod
    async def astream(self, messages: List[Any]) -> AsyncGenerator[Any, None]:
        pass
