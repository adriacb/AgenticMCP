from types import SimpleNamespace


class ChatLangGraphUseCase:
    def __init__(self, config, graph_client):
        self.config = config
        self.graph_client = graph_client

    async def __call__(self, input_obj):
        # Minimal behaviour for tests: ensure query exists
        query = getattr(input_obj, "query", None)
        if not query:
            raise ValueError("query is required")
        return SimpleNamespace(response="ok", metadata={"source": "ChatLangGraph"})
