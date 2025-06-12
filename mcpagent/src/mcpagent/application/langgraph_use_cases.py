from typing import Any, Dict, List, TypedDict, AsyncGenerator
from fastapi import WebSocket
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# Define our state
class AgentState(TypedDict):
    messages: List[Any]
    next: str

# Define our tools
@tool
def search(query: str) -> str:
    """Search for information about a topic."""
    return f"Search results for: {query}"

# Create the graph
def create_graph() -> Graph:
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=True
    )
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Define the nodes
    def generate_response(state: AgentState) -> AgentState:
        """Generate a response using the LLM."""
        messages = state["messages"]
        response = llm.invoke(messages)
        return {"messages": messages + [response], "next": "end"}
    
    # Add the nodes
    workflow.add_node("generate", generate_response)
    
    # Set the entry point
    workflow.set_entry_point("generate")
    
    # Compile the graph
    return workflow.compile()

# Create the graph instance
graph = create_graph()

# Non-streaming generation
async def generate_response(messages: List[Any]) -> Dict[str, Any]:
    """Generate a response without streaming."""
    state = {"messages": messages, "next": "generate"}
    result = await graph.ainvoke(state)
    return result

# Streaming generation
async def generate_stream(messages: List[Any]) -> AsyncGenerator[Dict[str, Any], None]:
    """Generate a response with streaming."""
    state = {"messages": messages, "next": "generate"}
    async for event in graph.astream(state):
        yield event

# WebSocket handler
async def handle_websocket(websocket: WebSocket, messages: List[Any]):
    """Handle WebSocket connection for streaming responses."""
    await websocket.accept()
    try:
        async for event in generate_stream(messages):
            await websocket.send_json(event)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close() 