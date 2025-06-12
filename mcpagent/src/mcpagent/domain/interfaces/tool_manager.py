from typing import List, Dict, Any, Union
from abc import ABC, abstractmethod

from mcp.server.fastmcp.tools.base import Tool as MCPTool
from mcpagent.domain.interfaces.tool import Tool
from mcpagent.domain.interfaces.mcp_client import MCPClientInterface

class ToolManager(ABC):
    """Interface for managing tools that can be used by the LLM."""
    
    @abstractmethod
    def add_tool(self, tool: Union[Tool, MCPTool]) -> None:
        """Add a tool to the repository."""
        pass
    
    @abstractmethod
    def get_tool(self, name: str) -> Union[Tool, MCPTool]:
        """Get a tool by name."""
        pass
    
    @abstractmethod
    def list_tools(self) -> List[Union[Tool, MCPTool]]:
        """List all tools in the repository."""
        pass
    
    @abstractmethod
    def get_llm_tools(self) -> List[Dict[str, Any]]:
        """Get all tools in a format suitable for the LLM."""
        pass
    
    @abstractmethod
    def remove_tool(self, name: str) -> None:
        """Remove a tool from the repository."""
        pass
    
    @abstractmethod
    def get_mcp_client(self) -> MCPClientInterface:
        """Get the MCP client for executing MCP tools."""
        pass 