# core/infrastructure/events/consumer.py
from mcpagent.core.application.use_cases.handle_event_chat import HandleEventChat
from mcpagent.core.application.dto.payloads import EventChatPayload
from mcpagent.core.domain.interfaces.event_queue_interface import EventQueueInterface

async def consume_events(event_queue: EventQueueInterface, graph, callbacks, logger):
    handler = HandleEventChat()

    async for event in event_queue.consume():  # works for InMemory or Kafka
        event_type = event["event_type"]
        payload = event["payload"]

        if event_type == "chat":
            payload = EventChatPayload(**payload)
            async for chunk in handler(graph=graph, event=payload, callbacks=callbacks):
                logger.debug(f"Streamed chunk: {chunk}")

        elif event_type == "email":
            # handle emails here
            pass
