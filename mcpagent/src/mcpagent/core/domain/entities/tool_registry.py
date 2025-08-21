from mcpagent.core.domain.interfaces import ToolRegistryInterface
from langchain_core.tools import StructuredTool
from .tool import Tool
from typing import Dict, Optional

class InMemoryToolRegistry(ToolRegistryInterface):
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def add(self, tool: Tool) -> None:
        """Register a tool in the registry."""
        if tool.name in self._tools:
            raise ValueError(f"Tool with name {tool.name} already exists.")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Retrieve a tool by its name."""
        return self._tools.get(name)
    
    def remove(self, name: str) -> None:
        """Remove a tool from the registry by its name."""
        if name in self._tools:
            del self._tools[name]
        else:
            raise ValueError(f"Tool with name {name} does not exist.")

    def list(self) -> list:
        """Return tools in LangChain-compatible format."""
        converted = []
        for tool in self._tools.values():
            # Wrap your domain Tool into a StructuredTool
            converted.append(
                StructuredTool.from_function(
                    func=tool.function,           # the actual Python function
                    name=tool.name,
                    description=tool.description,
                    args_schema=tool.args_schema  # <-- you must attach a Pydantic model here
                )
            )
        return converted