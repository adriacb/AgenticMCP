from typing import List, Union, Dict
from langchain.chat_models import init_chat_model

from mcpagent.core.domain.interfaces import LLMInterface, BaseMessage
from mcpagent.core.domain.value_objects import LLMConfig
from mcpagent.infrastructure.logger import LoggerInitializer
from .messages import AIMessage
#from .tool import Tool
from mcp.server.fastmcp.tools.base import Tool


MessageInput = Union[BaseMessage, Dict[str, str]]


class ChatLLM(LLMInterface):
    """
    Lightweight chat LLM wrapper for MCP.

    Responsibilities:
        - Pure LLM invocation (sync or async)
        - Converts BaseMessage or dict messages to LangChain format
        - Supports MCP tool binding **at initialization** via `tools` parameter
        - Supports synchronous and asynchronous text generation
    """

    def __init__(self, llm_config: LLMConfig, tools: List[Tool] | None = None) -> None:
        """
        Initialize the ChatLLM and bind tools in a single step.

        Args:
            llm_config: LLM configuration object
            tools: Optional list of MCP Tool objects to bind. Each Tool must implement
                   `to_openai_tool()` to be compatible with LangChain tool-calling.
        """
        self.llm_config = llm_config

        # Initialize the LLM and bind tools in one shot
        # Tests may monkeypatch `_initialize_llm` to return a fake model.
        if hasattr(self, "_initialize_llm"):
            try:
                # Prefer calling with the `tools` keyword if the patched function accepts it
                self.llm = self._initialize_llm(tools=tools)
            except TypeError:
                # Fallback for test shims that provide a no-arg initializer (lambda self: ...)
                self.llm = self._initialize_llm()
        else:
            self.llm = (
                init_chat_model(**self.llm_config.model_dump()).bind_tools(tools)
                if tools
                else init_chat_model(**self.llm_config.model_dump())
            )

        self.logger = LoggerInitializer.get_default_logger()

        # Preserve the identity of the tools list for callers/tests
        self.tools = tools

        self.logger.debug(
            "ChatLLM initialized",
            extra={
                "llm_config": self.llm_config,
                "tools": [getattr(t, "name", None) for t in self.tools] if self.tools else [],
            },
        )

    def _initialize_llm(self, tools: List[Tool] | None = None):
        """Default hook that returns the initialized llm. Tests can monkeypatch
        this method to return a fake model object."""

        return (
            init_chat_model(**self.llm_config.model_dump()).bind_tools(tools)
            if tools
            else init_chat_model(**self.llm_config.model_dump())
        )

    def invoke(self, messages: List[MessageInput]) -> AIMessage:
        """
        Synchronously invoke the LLM.

        Args:
            messages: List of BaseMessage or dict messages.

        Returns:
            AIMessage: Domain message returned by the LLM.
        """
        return self.llm.invoke(messages)

    async def ainvoke(self, messages: List[MessageInput]) -> AIMessage:
        """
        Asynchronously invoke the LLM.

        Args:
            messages: List of BaseMessage or dict messages.

        Returns:
            AIMessage: Domain message returned by the LLM.
        """
        return await self.llm.ainvoke(messages)


    def generate(self, prompt: str) -> str:
        """
        Synchronous text generation using the LLM.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text.
        """
        self.logger.debug("ChatLLM generate called", extra={"prompt": prompt[:round(len(prompt) * 0.1)]})
        return self.llm.generate(prompt)

    async def agenerate(self, prompt: str) -> str:
        """
        Asynchronous text generation using the LLM.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text.
        """
        self.logger.debug("ChatLLM agenerate called", extra={"prompt": prompt[:round(len(prompt) * 0.1)]})
        return await self.llm.agenerate(prompt)
