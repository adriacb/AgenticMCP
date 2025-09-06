from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from application.use_cases.create_agent import CreateAgent
from application.use_cases.load_mcp_tools import load_mcp_tools
from core.domain.entities import InMemoryToolRegistry
from core.domain.interfaces import ToolRegistryInterface

class CreateMcpAgent:
    """Use case to create an Agent that connects to an MCP server and loads its tools."""

    def __init__(self, tool_registry: ToolRegistryInterface | None = None):
        self.tool_registry = tool_registry or InMemoryToolRegistry()

    async def execute(
        self,
        name: str,
        description: str,
        mcp_server: str,
        llm_model: str = "gpt-4o-mini",
        temperature: float = 0.5,
        system_prompt_key: str = "retrieval_qa",
    ):
        server_params = StdioServerParameters(command="uv", args=["run", mcp_server])

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)

                for tool in tools:
                    self.tool_registry.add(tool)

                return CreateAgent(
                    tool_registry=self.tool_registry,
                    prompt_repository=InMemoryPromptRepository()
                )
