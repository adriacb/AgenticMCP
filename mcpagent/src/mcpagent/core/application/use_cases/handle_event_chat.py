from typing import AsyncGenerator, List, Callable
from mcpagent.infrastructure.langgraph.react_agent.states import State
from mcpagent.core.application.dto.payloads import EventChatPayload
from mcpagent.core.application.use_cases.langgraph.stream_response import stream_response
from mcpagent.infrastructure.logger import LoggerInitializer


class HandleEventChat:
    """Use case to handle a chat event."""

    logger = LoggerInitializer.get_default_logger()

    async def __call__(
        self,
        graph,
        event: EventChatPayload,
        callbacks: List[Callable] = [],
    ) -> AsyncGenerator[str, None]:
        """Handle a chat event and stream responses."""
        self.logger.info(f"Handling chat event for thread {event.thread_id}")

        # Convert EventChatPayload -> LangGraph State
        state = State(
            messages=[{"role": "user", "content": event.message}],
        )

        async for chunk in stream_response(graph=graph, state=state, callbacks=callbacks):
            yield chunk
