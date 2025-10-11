# core/application/services/event_queue_service.py
from mcpagent.core.domain.interfaces.event_queue_interface import EventQueueInterface
from mcpagent.core.application.use_cases.handle_event_chat import HandleEventChat
from mcpagent.core.application.dto.payloads import EventChatPayload

class EventQueueService:
    def __init__(self, event_queue: EventQueueInterface, graph, callbacks, logger):
        self.event_queue = event_queue
        self.graph = graph
        self.callbacks = callbacks
        self.logger = logger

    async def start(self):
        handler = HandleEventChat()
        async for event in self.event_queue.consume():
            event_type = event["event_type"]
            payload = event["payload"]

            if event_type == "chat":
                payload = EventChatPayload(**payload)
                async for chunk in handler(graph=self.graph, event=payload, callbacks=self.callbacks):
                    self.logger.debug(f"Streamed chunk: {chunk}")
