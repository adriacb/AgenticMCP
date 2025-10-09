import asyncio
from mcpagent.infrastructure.langgraph.react_agent.graph import ReACTGraph
from mcpagent.infrastructure.config.settings import load_settings

settings = load_settings("pro")
# Module-level placeholder for LangGraph
react_graph = None

config = {

    "math": {
        "transport": "stdio",
        "command": "uv",
        "args": ["run", "math_server.py"],
        "env": {"DEBUG": "true"},
        "cwd": "C:\\Users\\cabe\\Documents\\repos\\agentic_summits\\AgenticMCP\\notebooks\\mcp",
    }

}


async def main():
    global react_graph

    # Create and initialize the ReACTGraph instance
    graph = ReACTGraph(mcp_config=config)
    await graph._initialize()

    # Set the module-level variable for Studio (optional if you need it at runtime)
    react_graph = graph.graph

    # # Invoke the agent
    # result = await graph.invoke("sum 2 + 2 and multiply the result by 5")

    # # Print the last message prettily
    # result['messages'][-1].pretty_print()

    # # Save graph image
    # graph.save_graph_image("react_graph.png")

    react_graph = graph.graph


asyncio.run(main())


