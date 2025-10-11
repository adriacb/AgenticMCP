# core/infrastructure/queue/in_memory_event_queue.py
import asyncio
from mcpagent.core.domain.interfaces.event_queue_interface import EventQueueInterface
from typing import AsyncIterator

class InMemoryEventQueue(EventQueueInterface):
    def __init__(self):
        self._queue = asyncio.Queue()

    async def put(self, event: dict) -> None:
        await self._queue.put(event)

    async def consume(self) -> AsyncIterator[dict]:
        while True:
            event = await self._queue.get()
            yield event
