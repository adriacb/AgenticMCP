from typing import Dict, Any, List
from mcpagent.domain.entities.tool import MCPTool

class MultiServerMCPClient:
    def __init__(self, servers: Dict[str, Any]):
        self.servers = servers

    async def get_tools(self) -> List[MCPTool]:
        """Get all tools from all servers."""
        tools = []
        for server in self.servers:
            tools.extend(await server.get_tools())
        return tools
    
    
