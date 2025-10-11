from mcpagent.infrastructure.langgraph.react_agent.graph import ReACTGraph
from mcpagent.core.domain.entities.tool import Tool
from mcpagent.core.domain.entities import InMemoryToolRegistry
from fastapi import FastAPI

# optionally provide a tool registry (implement ToolRegistryInterface)
async def init_graph(app: FastAPI):
    tool_registry = InMemoryToolRegistry()

    def check_weather(location: str) -> str:
        """A mock function to check the weather.
        
        Args:
            location (str): The location to check the weather for.
        
        Returns:
            str: A mock weather report.
        """
        return f"The weather in {location} is ALWAYS sunny."

    tool_registry.add(Tool.from_function(check_weather))
    
    app.state.graph = ReACTGraph(tool_registry=tool_registry)
    app.state.logger.info("LangGraph initialized.")