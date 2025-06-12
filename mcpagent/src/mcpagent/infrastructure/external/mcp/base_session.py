from typing import Any, AsyncIterator, Optional
from mcpagent.domain.interfaces.session import StreamableSession

class BaseSession(StreamableSession):
    """Base session implementation."""
    
    def __init__(self, session_id: str):
        """Initialize the session.
        
        Args:
            session_id: Unique identifier for the session
        """
        self._session_id = session_id
        self._active = False
        self._read: Optional[Any] = None
        self._write: Optional[Any] = None
    
    @property
    def session_id(self) -> str:
        """Get the session ID."""
        return self._session_id
    
    async def start(self) -> None:
        """Start the session."""
        self._active = True
    
    async def close(self) -> None:
        """Close the session."""
        self._active = False
        if self._read:
            await self._read.aclose()
        if self._write:
            await self._write.aclose()
    
    async def is_active(self) -> bool:
        """Check if the session is active."""
        return self._active
    
    async def stream(self) -> AsyncIterator[Any]:
        """Stream data from the session."""
        if not self._active:
            raise RuntimeError("Session is not active")
        if not self._read:
            raise RuntimeError("No read stream available")
        
        async for chunk in self._read:
            yield chunk 