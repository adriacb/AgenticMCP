from types import SimpleNamespace


# Allow tests to monkeypatch the Agent symbol
Agent = None


class ChatAgentUseCase:
    """Minimal implementation used by unit tests.

    The real project may have a richer implementation; this shim provides
    the behavior that tests expect: call an Agent.invoke and return a
    SimpleNamespace with response and metadata.source == 'ChatAgent'.
    """

    def __init__(self, config, tool_registry):
        self.config = config
        self.tool_registry = tool_registry

    async def __call__(self, input_obj):
        query = getattr(input_obj, "query", None)
        if not query:
            raise ValueError("query is required")

        # Agent symbol is patched in tests; use it if present.
        Agent = globals().get("Agent")
        agent = Agent(self.config, self.tool_registry)
        response = await agent.invoke(query, tools=getattr(input_obj, "tools", None), context=getattr(input_obj, "context", None))

        return SimpleNamespace(response=response, metadata={"source": "ChatAgent"})
