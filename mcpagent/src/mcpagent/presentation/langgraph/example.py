import asyncio
from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver
from application.use_cases.create_mcp_agent import CreateMcpAgent


def agent_to_node(agent):
    async def node(state):
        response = agent.invoke(state["messages"])
        state["messages"].append({"role": "assistant", "content": response})
        return state
    return node


async def init_graph():
    """Initialize all agents and compile the LangGraph workflow."""
    create_mcp_agent = CreateMcpAgent()

    math_agent = await create_mcp_agent.execute(
        name="Math Assistant",
        description="Performs math calculations",
        mcp_server="math_server.py",
    )

    research_agent = await create_mcp_agent.execute(
        name="Research Assistant",
        description="Looks up academic papers",
        mcp_server="search_server.py",
    )

    graph = StateGraph({"messages": list})
    graph.add_node("math", agent_to_node(math_agent))
    graph.add_node("research", agent_to_node(research_agent))

    graph.add_edge("math", "research")
    graph.set_entry_point("math")
    graph.set_finish_point("research")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


# 👇 Global app instance (can be reused in API layer)
graph_app = asyncio.run(init_graph())
