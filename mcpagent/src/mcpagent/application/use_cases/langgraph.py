import json
import uuid
from typing import AsyncGenerator, List, Callable, Optional, Any
from mcpagent.application.services.logger import LoggerInitializer

logger = LoggerInitializer.get_default_logger()


def build_graph():
    """Build the graph."""
    raise NotImplementedError("Graph not implemented")
        
async def stream_response(graph: Any, 
                          query: str,
                          thread_id: str = None,
                          callbacks: Optional[List[Callable]] = None
                          ) -> AsyncGenerator[str, None]:
    """Stream the response from the graph.
    
    Args:
        graph: The graph to stream the response from.
        query: The query to stream the response for.
        thread_id: The thread ID to stream the response for.
        callbacks: The callbacks to use for the response.
    
    Returns:
        An async generator of the response.
    """
    logger.info(f"Streaming response for query: {query}")
    try:
        config = {"callbacks": callbacks} if callbacks else {}
        config["configurable"] = {"thread_id": thread_id if thread_id else str(uuid.uuid4())}

        # Stream the response with Langfuse monitoring
        async for _, s in graph.astream(
            {"messages": [("user", query)]},
            config=config,
            stream_mode=["messages"]
        ):
            msg, metadata = s
            logger.info(f"Message: {msg.content}")
            yield msg.content
            # if "messages" in chunk and chunk["messages"]:
            #     last_message = chunk["messages"][-1]
            #     yield last_message.content

    except Exception as e:
        logger.error("Error streaming response", exc_info=e)
        yield f"data: {json.dumps({'error': str(e)})}\n\n"