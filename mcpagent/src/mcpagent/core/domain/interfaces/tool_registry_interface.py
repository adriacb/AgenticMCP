from abc import ABC, abstractmethod
from .tool_interface import ToolInterface


class ToolRegistryInterface(ABC):
    @abstractmethod
    def get(self, name: str) -> dict:
        """Retrieve a tool by its ID."""
        pass

    @abstractmethod
    def add(self, tool: ToolInterface) -> None:
        """Add a new tool to the registry."""
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        """Remove a tool from the registry."""
        pass

    @abstractmethod
    def list(self) -> dict[str, ToolInterface]:
        """List all available tools."""
        pass
