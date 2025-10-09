import pytest
from mcpagent.core.domain.entities import Tool
from mcpagent.core.domain.value_objects import ToolCard
from mcpagent.core.domain.interfaces import ToolRegistryInterface


def test_tool_execute_calls_function_with_args_and_kwargs():
    called = {}

    def fn(*args, **kwargs):
        called["args"] = args
        called["kwargs"] = kwargs
        return "result-ok"

    card = ToolCard(
        name="demo-tool",
        description="demo",
        tags=["demo"],
        examples=["example"],
        parameters={"args": [1, 2], "kwargs": {"x": 3}},
        function=fn,
    )
    tool = Tool(tool_card=card)

    res = tool.execute()

    assert res == "result-ok"
    assert called["args"] == (1, 2)
    assert called["kwargs"] == {"x": 3}


def test_tool_repr_contains_name():
    def noop():
        pass

    card = ToolCard(name="mytool", description="d", parameters={}, function=noop)
    tool = Tool(tool_card=card)
    assert "mytool" in repr(tool)


def test_inmemory_tool_registry_add_get_remove_list():
    class InMemoryToolRegistry(ToolRegistryInterface):
        def __init__(self):
            self._store = {}

        def get(self, tool_id: str):
            return self._store.get(tool_id)

        def add(self, tool_id: str, tool_data: dict) -> None:
            self._store[tool_id] = tool_data

        def remove(self, tool_id: str) -> None:
            self._store.pop(tool_id, None)

        def list(self) -> list:
            return list(self._store.keys())

    registry = InMemoryToolRegistry()
    assert registry.list() == []

    registry.add("t1", {"name": "t1", "meta": 1})
    assert registry.get("t1") == {"name": "t1", "meta": 1}
    assert registry.list() == ["t1"]

    registry.remove("t1")
    assert registry.get("t1") is None
    assert registry.list() == []
