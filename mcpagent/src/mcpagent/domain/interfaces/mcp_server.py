"""        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/path/to/math_server.py"],
            "transport": "stdio",
        }"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod
from mcpagent.domain.entities.tool import MCPTool

class MCPServerInterface(ABC):
    @abstractmethod
    async def get_tools(self) -> List[MCPTool]:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
