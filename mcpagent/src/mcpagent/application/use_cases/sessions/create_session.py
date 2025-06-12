from typing import AsyncIterator
from mcpagent.domain.interfaces.connection import Connection
from mcpagent.domain.interfaces.session import Session, SessionFactory

class CreateSession:
    """Use case for creating a session based on connection configuration."""
    
    def __init__(self, session_factory: SessionFactory):
        """Initialize the use case.
        
        Args:
            session_factory: The session factory to use
        """
        self._session_factory = session_factory
    
    async def execute(self, connection: Connection) -> AsyncIterator[Session]:
        """Create a session based on the connection configuration.
        
        Args:
            connection: The connection configuration to use
            
        Returns:
            An async iterator that yields a Session
            
        Raises:
            ValueError: If the transport type is not supported
        """
        async for session in self._session_factory.create_session(connection):
            yield session 