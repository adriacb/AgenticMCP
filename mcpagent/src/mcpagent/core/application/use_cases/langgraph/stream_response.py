from typing import List, AsyncGenerator, Literal
from langgraph.graph import StateGraph

async def stream_response(
        graph: StateGraph, 
        state: State,
        stream_mode: Literal["updates", "messages", "custom"] = "messages",
        thread_id: str = "",
        callbacks: List[callable] = []
    ) -> AsyncGenerator[dict, None]:
    """
    Streams compiled LangGraph responses
    """
    async for message_chunk, _ in graph.astream( #metadata is not used
        state=state, 
        stream_mode=stream_mode,
        config = {"configurable": {"thread_id": thread_id, "callbacks": callbacks}}
    ):
        if message_chunk.content:
            yield(message_chunk.content)