import pytest
from types import SimpleNamespace

from mcpagent.core.domain.value_objects import AgentConfig, LLMConfig, AgentCard
from mcpagent.core.domain.entities import Agent
from mcpagent.core.domain.interfaces import ToolRegistryInterface

# create dummy data for testing
@pytest.fixture
def dummy_llm_config():
    return LLMConfig(model="gpt-4", temperature=0.5)

@pytest.fixture
def dummy_agent_card():
    return AgentCard(name="TestAgent", description="An agent that assists with tasks.")

@pytest.fixture
def dummy_agent_config(dummy_llm_config, dummy_agent_card):
    return AgentConfig(
        llm_config=dummy_llm_config,
        agent_card=dummy_agent_card,
        system_prompt="You are a helpful assistant."
    )
@pytest.fixture
def dummy_tool_registry():
    class DummyToolRegistry(ToolRegistryInterface):
        def __init__(self):
            pass
        def get(self, tool_name: str):
            return None
        def add(self, tool):
            pass
        def remove(self, tool_name: str):
            pass
        def list(self):
            return []

    return DummyToolRegistry()  

def test_agent_initialization(dummy_agent_config, dummy_tool_registry):
    # patch _init_llm to avoid real model init
    class DummyLLM:
        def __init__(self): pass
    dummy_llm = DummyLLM()
    from types import SimpleNamespace
    # monkeypatch before creating Agent
    import pytest as _pytest
    _pytest.monkeypatch = None  # noop to satisfy linter when running standalone

    # create Agent with patched _init_llm
    from unittest.mock import patch
    with patch.object(Agent, "_init_llm", return_value=dummy_llm):
        agent = Agent(config=dummy_agent_config, tool_registry=dummy_tool_registry)

    assert agent.config.llm_config.model == "gpt-4"
    assert agent.config.llm_config.temperature == 0.5
    assert agent.config.agent_card.name == "TestAgent"
    assert agent.config.agent_card.description == "An agent that assists with tasks."
    assert agent.tool_registry is not None
    assert isinstance(agent.tool_registry, ToolRegistryInterface)

def test_agent_invoke(dummy_agent_config, dummy_tool_registry, monkeypatch):
    # create a mock LLM with the methods Agent will call
    class MockLLM:
        def invoke(self, messages):
            return "mocked sync response"
        async def ainvoke(self, messages):
            return "mocked async response"

    mock_llm = MockLLM()
    # monkeypatch Agent._init_llm so Agent.llm is our mock
    monkeypatch.setattr(Agent, "_init_llm", lambda self: mock_llm)

    agent = Agent(config=dummy_agent_config, tool_registry=dummy_tool_registry)
    input_messages = ["Hello, how can you assist me?"]
    response = agent.invoke(input_messages)

    assert isinstance(response, str)
    assert response == "mocked sync response"