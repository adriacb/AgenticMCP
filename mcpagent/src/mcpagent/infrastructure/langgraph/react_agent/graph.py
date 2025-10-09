from typing import Dict, List, Any, Optional
import asyncio

from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_mcp_adapters.client import MultiServerMCPClient

from mcpagent.infrastructure.logger import LoggerInitializer
from mcpagent.infrastructure.langgraph.react_agent.states import InputState, State
from mcpagent.infrastructure.langgraph.react_agent.nodes import CallModelFunctionNode, route_model_output


class ReACTGraph:
    """
    ReACTGraph is a self-initializing LangGraph agent implementing the ReACT pattern.
    It manages MCP clients, merges local and MCP-provided tools, and builds the state graph.

    The graph is initialized automatically upon construction, so no separate `initialize` call is needed.

    Attributes:
        logger: Logger instance for internal messages.
        mcp_config: Optional configuration dictionary for MultiServerMCPClient.
        local_tools: Optional list of local tools or callables.
        mcp_client: Optional MCP client instance.
        graph: Compiled LangGraph StateGraph ready for invocation.
    """

    def __init__(
        self,
        mcp_config: Optional[Dict[str, Any]] = None,
        local_tools: Optional[List[Any]] = None,
    ):
        """
        Initialize ReACTGraph and automatically set up the MCP client, tools, and graph.

        Args:
            mcp_config: Optional dictionary defining MCP servers and transport configurations.
            local_tools: Optional list of local tools or LangChain-compatible callables.

        Raises:
            ValueError: If no tools are provided either via MCP config or local_tools.
        """
        self.logger = LoggerInitializer.get_default_logger()
        self.mcp_config = mcp_config
        self.local_tools = local_tools or []
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.graph = None

        # Run asynchronous initialization immediately
        #asyncio.run(self._initialize())

    async def _initialize(self):
        """
        Internal async method to initialize MCP client, fetch MCP tools, merge with local tools,
        and compile the LangGraph StateGraph.

        Raises:
            ValueError: If neither MCP nor local tools are provided.
        """
        mcp_tools: List[Any] = []

        if self.mcp_config:
            self.mcp_client = await self._set_mcp_client(self.mcp_config)
            mcp_tools = await self._set_tools()

        # Merge MCP and local tools
        tools = (mcp_tools or []) + (self.local_tools or [])

        if not tools:
            raise ValueError(
                "No tools provided. You must configure at least one MCP server or pass local_tools."
            )

        self.graph = self._build_graph(tools)

    async def _set_mcp_client(self, mcp_config: Dict[str, Any]) -> MultiServerMCPClient:
        """
        Initialize the MCP client using the provided configuration.

        Args:
            mcp_config: MCP server configuration dictionary.

        Returns:
            An instance of MultiServerMCPClient.

        Raises:
            Exception: If the MCP client fails to initialize.
        """
        try:
            return MultiServerMCPClient(mcp_config)
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP client: {e}")
            raise

    async def _set_tools(self) -> List[Any]:
        """
        Fetch tools from the MCP client asynchronously.

        Returns:
            A list of MCP-provided tools. Returns an empty list if no client exists or fetching fails.
        """
        print("==================")
        print(self.mcp_client)
        if self.mcp_client:
            try:
                return await self.mcp_client.get_tools()
            except Exception as e:
                self.logger.error(f"Failed to fetch tools: {e}")
                return []
        return []

    def _build_graph(self, tools: List[Any]):
        """
        Build the ReACT agent StateGraph with the provided tools.

        Args:
            tools: List of tools or callables to integrate into the graph.

        Returns:
            A compiled StateGraph ready for asynchronous invocation.
        """
        call_model = CallModelFunctionNode(tools=tools)

        builder = StateGraph(State, input=InputState)
        builder.add_node("call_model", call_model)
        builder.add_node("tools", ToolNode(tools))

        # Start flow
        builder.add_edge("__start__", "call_model")

        # Conditional routing from model output
        builder.add_conditional_edges("call_model", route_model_output)

        # Loop back to model after tools
        builder.add_edge("tools", "call_model")

        return builder.compile(name="ReAct Agent")

    def save_graph_image(self, filename="react_graph.png"):
        """
        Save a visual representation of the graph as a PNG file.

        Args:
            filename: Optional file name for the saved graph image (default: 'react_graph.png').
        """
        png_bytes = self.graph.get_graph().draw_mermaid_png()
        with open(filename, "wb") as f:
            f.write(png_bytes)
        print(f"Graph saved to {filename}")

    async def invoke(self, user_message: str):
        """
        Invoke the ReACT agent with a user message asynchronously.

        Args:
            user_message: The text message from the user to send to the agent.

        Returns:
            The agent's response as produced by the graph invocation.

        Raises:
            RuntimeError: If the graph was not successfully initialized (should not occur with self-initializing class).
        """
        if not self.graph:
            raise RuntimeError("Graph not initialized (should not happen).")

        return await self.graph.ainvoke(
            input=InputState(
                messages=[{"role": "user", "content": user_message}],
            )
        )


# from typing import Dict, List, Any, Optional
# import asyncio

# from langgraph.graph import StateGraph
# from langgraph.prebuilt import ToolNode
# from langchain_mcp_adapters.client import MultiServerMCPClient

# from mcpagent.infrastructure.logger import LoggerInitializer
# from mcpagent.infrastructure.langgraph.react_agent.states import InputState, State
# from mcpagent.infrastructure.langgraph.react_agent.nodes import CallModelFunctionNode, route_model_output


# class ReACTGraph:
#     """
#     Async-initialized ReACTGraph agent implementing the ReACT pattern.

#     This class manages MCP clients, merges local and MCP-provided tools, and builds a LangGraph
#     StateGraph that can be invoked asynchronously. Use the async factory method `create` to
#     initialize the agent.

#     Attributes:
#         logger: Logger instance for internal messages.
#         mcp_client: Optional MultiServerMCPClient instance.
#         local_tools: List of local tools provided by the user.
#         tools: Combined list of MCP and local tools.
#         graph: Compiled LangGraph StateGraph ready for invocation.
#     """

#     def __init__(
#         self,
#         mcp_client: Optional[MultiServerMCPClient] = None,
#         tools: Optional[List[Any]] = None,
#     ):
#         """
#         Private constructor. Initializes instance variables without performing async operations.

#         Args:
#             mcp_client: Optional pre-initialized MultiServerMCPClient.
#             tools: Optional list of tools to use in the graph.
#         """
#         self.logger = LoggerInitializer.get_default_logger()
#         self.mcp_client = mcp_client
#         self.local_tools: List[Any] = []
#         self.tools: List[Any] = tools or []
#         self.graph: Optional[StateGraph] = None

#     @classmethod
#     async def create(
#         cls,
#         mcp_config: Optional[Dict[str, Any]] = None,
#         local_tools: Optional[List[Any]] = None,
#     ) -> "ReACTGraph":
#         """
#         Async factory method to create a fully initialized ReACTGraph.

#         This method performs all async initialization:
#         - Sets up MCP client if `mcp_config` is provided.
#         - Fetches MCP tools asynchronously.
#         - Merges MCP tools with local tools.
#         - Builds the LangGraph StateGraph.

#         Args:
#             mcp_config: Optional dictionary defining MCP servers and transport configurations.
#             local_tools: Optional list of local tools or LangChain-compatible callables.

#         Returns:
#             A fully initialized ReACTGraph instance.

#         Raises:
#             ValueError: If no tools are provided either via MCP or local tools.
#         """
#         instance = cls()
#         instance.local_tools = local_tools or []

#         mcp_tools: List[Any] = []

#         if mcp_config:
#             instance.mcp_client = await instance._set_mcp_client(mcp_config)
#             mcp_tools = await instance._set_tools()

#         # Merge MCP and local tools
#         instance.tools = (mcp_tools or []) + (instance.local_tools or [])

#         if not instance.tools:
#             raise ValueError(
#                 "No tools provided. You must configure at least one MCP server or pass local_tools."
#             )

#         instance.graph = instance._build_graph(instance.tools)
#         return instance

#     async def _set_mcp_client(self, mcp_config: Dict[str, Any]) -> MultiServerMCPClient:
#         """
#         Initialize the MCP client asynchronously.

#         Args:
#             mcp_config: MCP server configuration dictionary.

#         Returns:
#             A MultiServerMCPClient instance.

#         Raises:
#             Exception: If the MCP client fails to initialize.
#         """
#         try:
#             return MultiServerMCPClient(mcp_config)
#         except Exception as e:
#             self.logger.error(f"Failed to initialize MCP client: {e}")
#             raise

#     async def _set_tools(self) -> List[Any]:
#         """
#         Fetch tools from the MCP client asynchronously.

#         Returns:
#             A list of MCP-provided tools. Returns an empty list if no client exists or fetching fails.
#         """
#         if self.mcp_client:
#             try:
#                 return await self.mcp_client.get_tools()
#             except Exception as e:
#                 self.logger.error(f"Failed to fetch tools: {e}")
#                 return []
#         return []

#     def _build_graph(self, tools: List[Any]) -> StateGraph:
#         """
#         Build the ReACT agent StateGraph with the provided tools.

#         Args:
#             tools: List of tools or callables to integrate into the graph.

#         Returns:
#             A compiled LangGraph StateGraph ready for asynchronous invocation.
#         """
#         call_model = CallModelFunctionNode(tools=tools)

#         builder = StateGraph(State, input=InputState)
#         builder.add_node("call_model", call_model)
#         builder.add_node("tools", ToolNode(tools))

#         # Start flow
#         builder.add_edge("__start__", "call_model")

#         # Conditional routing from model output
#         builder.add_conditional_edges("call_model", route_model_output)

#         # Loop back to model after tools
#         builder.add_edge("tools", "call_model")

#         return builder.compile(name="ReAct Agent")

#     def save_graph_image(self, filename: str = "react_graph.png") -> None:
#         """
#         Save a visual representation of the graph as a PNG file.

#         Args:
#             filename: Optional file name for the saved graph image (default: 'react_graph.png').
#         """
#         png_bytes = self.graph.get_graph().draw_mermaid_png()
#         with open(filename, "wb") as f:
#             f.write(png_bytes)
#         self.logger.info(f"Graph saved to {filename}")

#     async def invoke(self, user_message: str) -> Any:
#         """
#         Invoke the ReACT agent with a user message asynchronously.

#         Args:
#             user_message: The text message from the user to send to the agent.

#         Returns:
#             The agent's response as produced by the graph invocation.

#         Raises:
#             RuntimeError: If the graph was not successfully initialized.
#         """
#         if not self.graph:
#             raise RuntimeError("Graph not initialized (should not happen).")

#         return await self.graph.ainvoke(
#             input=InputState(messages=[{"role": "user", "content": user_message}])
#         )
