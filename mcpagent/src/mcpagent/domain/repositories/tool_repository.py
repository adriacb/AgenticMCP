from abc import ABC, abstractmethod
from typing import List, Optional

from mcpagent.domain.entities.tool import Tool

class ToolRepository(ABC):
    """Repository interface for managing tools."""
    
    @abstractmethod
    def save(self, tool: Tool) -> None:
        """Save a tool to the repository."""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Tool]:
        """List all tools in the repository."""
        pass
    
    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete a tool from the repository."""
        pass 