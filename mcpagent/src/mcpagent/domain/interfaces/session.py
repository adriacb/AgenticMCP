from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Protocol

class Session(Protocol):
    """Interface for MCP sessions."""
    
    async def initialize(self) -> None:
        """Initialize the session."""
        ...
    
    async def is_active(self) -> bool:
        """Check if the session is active."""
        ...
    
    async def get_tools(self) -> list[Any]:
        """Get a list of tools from the session."""
        ...
    
    async def get_prompt(self, name: str, *, arguments: dict[str, Any] | None = None) -> list[Any]:
        """Get a prompt from the session.
        
        Args:
            name: Name of the prompt to get
            arguments: Optional arguments to pass to the prompt
        """
        ...
    
    async def get_resources(self, *, uris: str | list[str] | None = None) -> list[Any]:
        """Get resources from the session.
        
        Args:
            uris: Optional resource URI or list of URIs to load. If not provided, all resources will be loaded.
        """
        ...

class StreamableSession(Session):
    """Interface for sessions that support streaming."""
    
    @abstractmethod
    async def stream(self) -> AsyncIterator[Any]:
        """Stream data from the session."""
        pass

class SessionFactory(Protocol):
    """Protocol for session factory."""
    async def create_session(self, connection: Any) -> AsyncIterator[Session]: ... 