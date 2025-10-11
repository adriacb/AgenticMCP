# core/infrastructure/queue/kafka_event_queue.py
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from mcpagent.core.domain.interfaces.event_queue_interface import EventQueueInterface
from typing import AsyncIterator

class KafkaEventQueue(EventQueueInterface):
    def __init__(self, servers: str, topic: str):
        self._servers = servers
        self._topic = topic
        self._producer = AIOKafkaProducer(bootstrap_servers=servers)
        self._consumer = AIOKafkaConsumer(topic, bootstrap_servers=servers, group_id="agentic_consumer")

    async def start(self):
        await self._producer.start()
        await self._consumer.start()

    async def stop(self):
        await self._producer.stop()
        await self._consumer.stop()

    async def put(self, event: dict) -> None:
        await self._producer.send_and_wait(self._topic, json.dumps(event).encode())

    async def consume(self) -> AsyncIterator[dict]:
        async for msg in self._consumer:
            yield json.loads(msg.value)
