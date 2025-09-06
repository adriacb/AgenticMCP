from typing import List
from mcpagent.core.domain.value_objects import AgentConfig
from mcpagent.core.domain.interfaces import BaseMessage, AgentInterface
from mcpagent.core.application.dto import ToolMessage
from mcpagent.src.mcpagent.infrastructure import logger
# We'll construct our framework-agnostic ToolMessage DTO for clarity, but
# convert it to a plain dict with `to_dict()` before appending so LangChain
# can coerce the message correctly.
from .messages import AIMessage
from .llm import ChatLLM
from fastmcp.tools import Tool
from fastmcp import Client
from mcp import ClientSession
from mcpagent.infrastructure.logger import LoggerInitializer


def fastmcp_tool_to_openai(tool: Tool) -> dict:
    dumped = tool.model_dump()

    return {
        "type": "function",
        "function": {
            "name": dumped["name"],
            "description": dumped.get("description", ""),
            "parameters": dumped.get("inputSchema", {}),  # ✅ use inputSchema
        },
    }


class MCPAgent(AgentInterface):
    def __init__(self, config: AgentConfig, session: ClientSession, tools: list[Tool]):
        self.config = config
        self.session = session
        self.tools = tools
        self.openai_tools = [fastmcp_tool_to_openai(t) for t in self.tools]
        self.llm = ChatLLM(config.llm_config, tools=self.openai_tools)
        self.logger = LoggerInitializer.get_default_logger()

    @classmethod
    async def create(cls, config: AgentConfig, session: ClientSession) -> "MCPAgent":
        """Async factory to fetch and wrap tools from MCP server."""
        try:
            tools = await session.list_tools()
            
        except Exception as e:
            cls.logger.error("Error fetching tools", extra={"error": e})
            tools = []
        return cls(config, session, tools)

    def format_prompt(self, messages: list) -> None:
        jsonified_tools = [tool.model_dump() for tool in self.tools]
        tool_names = [tool.name for tool in self.tools]

        return self.config.system_prompt.format(
            tools=jsonified_tools,
            chat_history=messages,
            input=messages[-1]["content"]
        )

    async def ainvoke(self, input: List[BaseMessage], max_attempts: int = 8) -> str:
        """Invoke the LLM and resolve tool calls up to `max_attempts` cycles.

        Behavior:
        - Build the prompt and call the LLM once.
        - If the LLM returns tool calls, execute them via `_handle_tool_calls()`
          which appends tool outputs and re-invokes the LLM.
        - Repeat until there are no tool calls or we've reached `max_attempts`.

        `max_attempts` counts the number of tool-handling cycles (not the total
        number of LLM calls). Pass `max_attempts=1` to keep strictly single-cycle
        behavior.
        """
        prompt = self.format_prompt(input)
        messages = [{"role": "assistant", "content": prompt}] + input
        self.logger.info("Messages before LLM call", extra={"messages": messages})

        # Initial LLM call
        result: AIMessage = await self.llm.ainvoke(messages)
        self.logger.info("LLM returned result", extra={"result": result})

        attempts = 0
        # Loop while the LLM returns tool calls and we have attempts left
        while getattr(result, "tool_calls", None) and attempts < max_attempts:
            self.logger.info("LLM requested tool calls; handling", extra={"attempt": attempts + 1})
            result = await self._handle_tool_calls(result, messages)
            self.logger.info("Result after handling tools", extra={"result": result})
            attempts += 1

        if getattr(result, "tool_calls", None):
            # max attempts reached and the LLM still wants to call tools.
            self.logger.warning("Max attempts reached while resolving tool calls", extra={"attempts": attempts})
            return getattr(result, "content", "Max attempts reached while resolving tool calls")

        # No remaining tool calls — return final assistant content
        return getattr(result, "content", "")

    def invoke(self, input: List[BaseMessage]) -> str:
        raise NotImplementedError("Synchronous invoke is not implemented. Use ainvoke instead.")

    async def _handle_tool_calls(self, result: AIMessage, messages: List[BaseMessage]) -> AIMessage:
        tool_calls = getattr(result, "tool_calls", [])
        if not tool_calls:
            return result

        self.logger.info("Handling tool calls", tool_calls=tool_calls)

        messages.append(result)

        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call.get("args", {}) or {}
            tool_call_id = call["id"]

            try:
                # Execute the tool via MCP session
                tool_result = await self.session.call_tool(tool_name, tool_args)
                tool_content = getattr(tool_result, "text", str(tool_result))
            except Exception as e:
                tool_content = f"[Error calling tool '{tool_name}': {e}]"

            # Create our DTO and append a serializable dict for the LLM
            tool_msg = ToolMessage(
                role="tool",
                tool_call_id=tool_call_id,
                name=tool_name,
                content=tool_content,
            )
            messages.append(tool_msg.to_dict())

        # Send updated messages back to LLM
        final_result: AIMessage = await self.llm.ainvoke(messages)
        return final_result
