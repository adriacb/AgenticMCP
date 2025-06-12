from abc import ABC, abstractmethod
from typing import Any, List, Optional

from mcpagent.domain.interfaces.connection import Connection
from mcpagent.domain.interfaces.session import Session

class ToolLoader(ABC):
    """Interface for loading tools from an MCP session."""
    
    @abstractmethod
    async def load_tools(
        self,
        session: Optional[Session] = None,
        *,
        connection: Optional[Connection] = None,
    ) -> List[Any]:
        """Load tools from an MCP session or connection.
        
        Args:
            session: Optional existing session to load tools from
            connection: Optional connection to create a new session from
            
        Returns:
            A list of tools
            
        Raises:
            ValueError: If neither session nor connection is provided
        """
        pass 