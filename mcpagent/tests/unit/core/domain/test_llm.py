import pytest

from mcpagent.core.domain.value_objects import LLMConfig
from mcpagent.core.domain.entities import ChatLLM
from mcpagent.core.domain.interfaces import ToolRegistryInterface

@pytest.fixture
def dummy_llm_config():
    return LLMConfig(model="gpt-4", temperature=0.5)

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

def test_llm_initialization(dummy_llm_config, monkeypatch):
    class DummyModel:
        def __init__(self, *args, **kwargs): pass
        def bind_tools(self, tools): return self

    # patch the class method directly (no module import)
    monkeypatch.setattr(ChatLLM, "_initialize_llm", lambda self: DummyModel())

    llm = ChatLLM(llm_config=dummy_llm_config)
    assert isinstance(llm.llm, DummyModel)

def test_llm_with_tool_registry(dummy_llm_config, dummy_tool_registry, monkeypatch):
    class DummyModel:
        def __init__(self, *args, **kwargs):
            pass
        def bind_tools(self, tools):
            return self

    monkeypatch.setattr(ChatLLM, "_initialize_llm", lambda self: DummyModel())
    llm = ChatLLM(llm_config=dummy_llm_config, tool_registry=dummy_tool_registry)
    assert isinstance(llm.llm, DummyModel)
    assert llm.tool_registry is dummy_tool_registry