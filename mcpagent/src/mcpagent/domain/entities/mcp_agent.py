from typing import Any, List, AsyncGenerator

from mcpagent.domain.interfaces.config import AgentConfig
from mcpagent.domain.interfaces.agent import AgentInterface
from mcpagent.domain.interfaces.llm import LLMInterface
from mcpagent.domain.interfaces.tool import ToolRepository

class MCPAgent(AgentInterface):
    """MCPAgent is an agent that can be used to interact with the MCP."""
    
    def __init__(self, 
                 config: AgentConfig,
                 llm: LLMInterface,
                 tools: ToolRepository
                 ):
        """Initialize the MCPAgent."""
        self.config = config
        self.llm = llm
        self.tools = tools

    async def ainvoke(self, messages: List[Any]) -> Any:
        """Invoke the agent with a list of messages."""
        pass


    async def astream(self, messages: List[Any]) -> AsyncGenerator[Any, None]:
        """Stream the agent's response to the client."""
        pass
