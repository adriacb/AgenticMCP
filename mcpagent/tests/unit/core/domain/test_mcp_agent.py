import asyncio
from types import SimpleNamespace
import importlib

MODULE_PATH = "mcpagent.core.domain.entities.mcp_agent"


def _patch_chatllm(module, fake_cls):
    setattr(module, "ChatLLM", fake_cls)


def test_ainvoke_without_tools_returns_llm_response():
    mod = importlib.import_module(MODULE_PATH)

    class FakeChatLLM:
        def __init__(self, llm_config, tools=None):
            self.calls = 0

        async def ainvoke(self, messages):
            self.calls += 1
            return SimpleNamespace(content="hello", tool_calls=[])

    _patch_chatllm(mod, FakeChatLLM)

    # Minimal config
    from mcpagent.core.domain.value_objects.agent_config import AgentConfig
    from mcpagent.core.domain.value_objects.llm_config import LLMConfig
    from mcpagent.core.domain.value_objects.agent_card import AgentCard

    cfg = AgentConfig(llm_config=LLMConfig(model="dummy"), agent_card=AgentCard())

    # simple session stub
    session = SimpleNamespace()

    agent = mod.MCPAgent(cfg, session, tools=[])

    result = asyncio.run(agent.ainvoke([{"role": "user", "content": "hi"}]))
    assert isinstance(result, str)
    assert "hello" in result


def test_ainvoke_with_tool_call_executes_tool_and_returns_final_response():
    mod = importlib.import_module(MODULE_PATH)

    class FakeChatLLM:
        def __init__(self, llm_config, tools=None):
            self._calls = 0

        async def ainvoke(self, messages):
            # first call returns a tool_call, second call returns final answer
            self._calls += 1
            if self._calls == 1:
                return SimpleNamespace(content="", tool_calls=[{"name": "add", "args": {"a": 2, "b": 2}, "id": "call1"}])
            return SimpleNamespace(content="The result of 2 + 2 is 4.", tool_calls=[])

    _patch_chatllm(mod, FakeChatLLM)

    # Create a session stub that implements async call_tool
    class FakeSession:
        async def call_tool(self, name, args):
            # emulate a tool result object with a .text attribute
            return SimpleNamespace(text=str(args.get("a", 0) + args.get("b", 0)))

    from mcpagent.core.domain.value_objects.agent_config import AgentConfig
    from mcpagent.core.domain.value_objects.llm_config import LLMConfig
    from mcpagent.core.domain.value_objects.agent_card import AgentCard
    cfg = AgentConfig(llm_config=LLMConfig(model="dummy"), agent_card=AgentCard())
    session = FakeSession()

    # Provide a fake Tool with model_dump() and name so fastmcp_tool_to_openai works
    class FakeTool:
        def __init__(self, name: str):
            self.name = name

        def model_dump(self):
            return {"name": self.name, "inputSchema": {}}

    agent = mod.MCPAgent(cfg, session, tools=[FakeTool("add")])

    result = asyncio.run(agent.ainvoke([{"role": "user", "content": "What is 2 + 2?"}]))
    assert isinstance(result, str)
    assert "4" in result
