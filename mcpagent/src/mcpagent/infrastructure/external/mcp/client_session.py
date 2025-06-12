from typing import Any, AsyncIterator, Optional
import asyncio
from .base_session import BaseSession

class ClientSession(BaseSession):
    """Base client session that uses read/write streams for communication."""
    
    def __init__(
        self,
        read: asyncio.StreamReader,
        write: asyncio.StreamWriter,
        session_kwargs: Optional[dict[str, Any]] = None,
    ):
        """Initialize the client session.
        
        Args:
            read: Stream reader for receiving messages
            write: Stream writer for sending messages
            session_kwargs: Optional session configuration
        """
        super().__init__(session_id="client_session")
        self._read = read
        self._write = write
        self._session_kwargs = session_kwargs or {}
    
    async def start(self) -> None:
        """Start the client session."""
        if self._active:
            return
        await super().start()
    
    async def close(self) -> None:
        """Close the client session."""
        if not self._active:
            return
        self._write.close()
        await self._write.wait_closed()
        await super().close()
    
    async def stream(self) -> AsyncIterator[Any]:
        """Stream messages from the client session."""
        if not self._active:
            raise RuntimeError("Session is not active")
            
        while True:
            try:
                message = await self._read.read(1024)
                if not message:
                    break
                yield message
            except asyncio.CancelledError:
                break
    
    async def send(self, message: str | bytes) -> None:
        """Send a message through the client session.
        
        Args:
            message: The message to send
        """
        if not self._active:
            raise RuntimeError("Session is not active")
            
        if isinstance(message, str):
            message = message.encode()
        self._write.write(message)
        await self._write.drain() 