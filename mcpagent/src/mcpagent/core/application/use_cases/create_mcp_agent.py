from fastmcp import Client
from mcpagent.core.domain.value_objects import AgentConfig
from mcpagent.core.domain.entities import MCPAgent


class CreateMcpAgent:
    """
    Use case for creating an MCPAgent instance.
    Encapsulates the creation logic and isolates external dependencies (like MCP session).
    """

    def __init__(self, agent_config: AgentConfig, session: Client):
        self._agent_config = agent_config
        self._session = session

    async def execute(self) -> MCPAgent:
        """
        Creates an MCPAgent using the provided config and MCP session.

        Returns:
            MCPAgent: The initialized agent.
        """
        return await MCPAgent.create(self._agent_config, self._session)
