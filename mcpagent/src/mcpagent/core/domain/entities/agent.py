from typing import List
from mcpagent.core.domain.interfaces import ToolRegistryInterface, BaseMessage
from mcpagent.core.domain.value_objects import AgentConfig
from mcpagent.core.application.dto import ToolMessage
from .messages import AIMessage
from .llm import ChatLLM
from mcpagent.infrastructure.logger import LoggerInitializer

logger = LoggerInitializer.get_default_logger()


class Agent:
    """
    Agent that uses ChatLLM and executes tools from a local ToolRegistry.

    Tool execution is done locally. ChatLLM only handles normalized messages.
    """

    def __init__(self, config: AgentConfig, tool_registry: ToolRegistryInterface):
        self.config = config
        self.tool_registry = tool_registry
        # Initialize the LLM (tests may monkeypatch `_init_llm` at the class level)
        self.llm = self._init_llm()

    def _init_llm(self):
        """Default LLM initializer. Tests can monkeypatch this method to
        inject a fake LLM instance before constructing Agent."""
        return ChatLLM(self.config.llm_config)

    def invoke(self, input: List[BaseMessage]) -> str:
        # synchronous wrapper used in tests
        return self.llm.invoke(input)

    async def ainvoke(self, input: List[BaseMessage]) -> AIMessage:
        """
        Main async entry point.

        Args:
            input: List of BaseMessage instances representing the conversation.

        Returns:
            AIMessage with all tool calls resolved.
        """
        messages = [{"role": "assistant", "content": self.config.system_prompt}] + input

        result: AIMessage = await self.llm.ainvoke(messages)
        final: AIMessage = await self._handle_tool_calls(result, messages)
        return final

    async def _handle_tool_calls(
        self, result: AIMessage, messages: List[BaseMessage]
    ) -> AIMessage:
        """
        Process tool calls from LLM output by executing local tools.

        Args:
            result: AIMessage returned by the LLM.
            messages: Conversation messages so far.

        Returns:
            AIMessage after tool calls have been executed.
        """
        tool_calls = getattr(result, "tool_calls", [])
        if not tool_calls:
            return result

        messages.append(result)

        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call.get("args", {}) or {}
            tool_call_id = call["id"]

            logger.debug("Executing local tool", extra={"tool": tool_name, "args": tool_args})

            tool = self.tool_registry.get(tool_name)
            if not tool:
                tool_output = f"[Error: tool '{tool_name}' not found]"
            else:
                try:
                    tool_output = tool.execute(**tool_args)
                except Exception as e:
                    tool_output = f"[Error executing '{tool_name}': {e}]"

            messages.append(
                ToolMessage(
                    role="tool",
                    name=tool_name,
                    tool_call_id=tool_call_id,
                    content=str(tool_output),
                )
            )

        return await self.llm.ainvoke(messages)
