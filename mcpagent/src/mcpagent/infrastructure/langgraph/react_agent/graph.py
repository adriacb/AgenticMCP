from typing import Dict, List, Any, Optional
import asyncio
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from mcpagent.core.domain.interfaces.tool_registry_interface import ToolRegistryInterface
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

    def __init__(self, tool_registry: ToolRegistryInterface):
        self.logger = LoggerInitializer.get_default_logger()
        self.tool_registry = tool_registry
        self.graph = self._build_graph(tool_registry.get_all_functions()) # LangGraph needs a list of tools to use in the ToolNode

    def _build_graph(self, tools: List[Any]):
        """
        Build the ReACT agent StateGraph with the provided tools.

        Args:
            tools: List of tools or callables to integrate into the graph.

        Returns:
            A compiled StateGraph ready for asynchronous invocation.
        """
        call_model = CallModelFunctionNode(tools=tools)

        builder = StateGraph(State, input_schema=InputState)
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

    def get_graph(self):
        return self.graph

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

    async def astream(self, state: dict):
        """
        Stream the ReACT agent's response asynchronously.
        """
        if not self.graph:
            raise RuntimeError("Graph not initialized (should not happen).")
        return await self.graph.astream(
            **state,
            stream_mode="messages",
        )
