from mcpagent.infrastructure.queue.in_memory_event_queue import InMemoryEventQueue
# from mcpagent.infrastructure.queue.kafka_event_queue import KafkaEventQueue
from fastapi import FastAPI

async def init_event_queue(app: FastAPI):
    app.state.event_queue = InMemoryEventQueue()
    # app.state.event_queue = KafkaEventQueue(servers=app.state.config.KAFKA_SERVERS, topic=app.state.config.KAFKA_TOPIC)
    app.state.logger.info(f"{app.state.event_queue.__class__.__name__} initialized.")