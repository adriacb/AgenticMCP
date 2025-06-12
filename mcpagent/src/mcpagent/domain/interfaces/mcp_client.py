from abc import ABC, abstractmethod
from typing import Any, List
from mcp.server.fastmcp.tools.base import Tool as MCPTool

class MCPClientInterface(ABC):
    """Interface for the MCP client that executes MCP tools."""
    
    @abstractmethod
    def execute_tool(self, tool: MCPTool, **kwargs) -> Any:
        """Execute an MCP tool with the given parameters."""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[MCPTool]:
        """Get all available MCP tools."""
        pass
    
    @abstractmethod
    def get_tool_by_name(self, name: str) -> MCPTool:
        """Get an MCP tool by name."""
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the MCP."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the MCP connection."""
        pass
