from typing import List, AsyncGenerator, Literal
from langgraph.graph import StateGraph
from pydantic import BaseModel

class State(BaseModel):
    messages: List[dict]
    metadata: dict

async def stream_response(
        graph: StateGraph,
        state: State,
        stream_mode: Literal["updates", "messages", "custom"] = "messages",
        thread_id: str = "",
        callbacks: List[callable] = []
    ) -> AsyncGenerator[dict, None]:
    """
    Streams compiled LangGraph responses asynchronously.
    
    Args:
        graph: The compiled StateGraph.
        state: The input state for the graph.
        stream_mode: Type of streaming ("updates", "messages", "custom").
        thread_id: Optional thread identifier.
        callbacks: Optional callbacks for streaming events.

    Yields:
        dict: Each chunk of the response content.
    """
    # astream returns an async generator, so we must async for it
    async for chunk in graph.graph.astream(state):
        yield chunk