import pytest
from types import SimpleNamespace

from mcpagent.core.application.use_cases import ChatAgentUseCase

@pytest.mark.asyncio
async def test_chat_agent_usecase_success(monkeypatch):
    # Dummy Agent implementation used to patch the real Agent dependency
    class DummyAgent:
        def __init__(self, config, tool_registry):
            self.config = config
            self.tool_registry = tool_registry

        async def invoke(self, query, tools=None, context=None):
            return "mocked-response"

    # Patch the Agent symbol used inside the use case module
    monkeypatch.setattr(
        "mcpagent.core.application.use_cases.chat_agent_use_case.Agent",
        DummyAgent,
    )

    usecase = ChatAgentUseCase(config=SimpleNamespace(), tool_registry=SimpleNamespace())
    input_obj = SimpleNamespace(query="Hello", tools=None, context=None)

    output = await usecase(input_obj)

    assert hasattr(output, "response")
    assert output.response == "mocked-response"
    assert getattr(output, "metadata", {}).get("source") == "ChatAgent"

@pytest.mark.asyncio
async def test_chat_agent_usecase_empty_query_raises(monkeypatch):
    class DummyAgent:
        def __init__(self, config, tool_registry):
            pass
        async def invoke(self, query, tools=None, context=None):
            return "should-not-be-returned"

    monkeypatch.setattr(
        "mcpagent.core.application.use_cases.chat_agent_use_case.Agent",
        DummyAgent,
    )

    usecase = ChatAgentUseCase(config=SimpleNamespace(), tool_registry=SimpleNamespace())
    input_obj = SimpleNamespace(query="", tools=None, context=None)

    with pytest.raises(ValueError):
        await usecase(input_obj)