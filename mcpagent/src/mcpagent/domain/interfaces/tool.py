from typing import Any, Dict
from abc import ABC, abstractmethod


class ToolInterface(ABC):
    """Interface for tools that can be used by the LLM."""
    
    @property
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the tool."""
        pass
    
    @property
    @abstractmethod
    def get_description(self) -> str:
        """Get the description of the tool."""
        pass
    
    @property
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get the parameters schema for the tool."""
        pass
