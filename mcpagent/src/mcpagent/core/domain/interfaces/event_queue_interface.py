# core/domain/interfaces/event_queue_interface.py
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

class EventQueueInterface(ABC):
    """Abstract interface for event queues."""

    @abstractmethod
    async def put(self, event: dict) -> None:
        """Publish an event to the queue."""
        pass

    @abstractmethod
    async def consume(self) -> AsyncIterator[dict]:
        """Consume events from the queue (as an async iterator)."""
        pass
