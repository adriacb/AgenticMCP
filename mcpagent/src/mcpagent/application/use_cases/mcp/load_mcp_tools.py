from typing import List, Any

from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.tool_loader import ToolLoader

class LoadMCPToolsUseCase:
    """Use case for loading tools from an MCP session."""
    
    def __init__(self, tool_loader: ToolLoader):
        """Initialize the use case.
        
        Args:
            tool_loader: The tool loader to use
        """
        self._tool_loader = tool_loader
    
    async def execute(
        self,
        session: Session,
    ) -> List[Any]:
        """Load tools from an MCP session.
        
        Args:
            session: Session to load tools from
            
        Returns:
            A list of tools
            
        Raises:
            ValueError: If session is inactive
        """
        if not await session.is_active():
            raise ValueError("Session is not active")
            
        return await self._tool_loader.load_tools(session=session) 