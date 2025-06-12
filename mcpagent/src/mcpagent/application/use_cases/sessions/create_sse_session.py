from typing import AsyncIterator, Any
from ....domain.interfaces.connection import SSEConnection
from ....domain.interfaces.session import Session
from ....domain.entities.mcp_session import McpSession
from ....infrastructure.external.mcp.constants import (
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT
)

class CreateSSESession:
    """Use case for creating an SSE session."""
    
    def __init__(self, session_factory: Any):  # We'll define the proper type when implementing the infrastructure
        self._session_factory = session_factory
    
    async def execute(self, connection: SSEConnection) -> AsyncIterator[Session]:
        """Create an SSE session.
        
        Args:
            connection: The SSE connection configuration
            
        Returns:
            An async iterator that yields a Session
            
        Raises:
            ValueError: If required parameters are missing
        """
        if "url" not in connection:
            raise ValueError("'url' parameter is required for SSE connection")
            
        # Use default values if not provided
        timeout = connection.get("timeout", DEFAULT_HTTP_TIMEOUT)
        sse_read_timeout = connection.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT)
        
        # Create the session using the factory
        async with self._session_factory.create_sse_session(
            url=connection["url"],
            headers=connection.get("headers"),
            timeout=timeout,
            sse_read_timeout=sse_read_timeout,
            session_kwargs=connection.get("session_kwargs"),
            httpx_client_factory=connection.get("httpx_client_factory"),
        ) as (read, write):
            session = McpSession(session_id=f"sse_{connection['url']}")
            session._read = read
            session._write = write
            await session.start()
            yield session 