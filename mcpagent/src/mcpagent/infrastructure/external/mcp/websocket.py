from typing import Any, AsyncIterator, Optional
from contextlib import asynccontextmanager
from mcp import ClientSession


@asynccontextmanager
async def create_websocket_session(
    url: str,
    session_kwargs: Optional[dict[str, Any]] = None,
) -> AsyncIterator[ClientSession]:
    """Create a new session to an MCP server using Websockets

    Args:
        url: URL of the Websocket endpoint
        session_kwargs: Additional keyword arguments to pass to the ClientSession

    Raises:
        ImportError: If websockets package is not installed
    """
    try:
        from mcp.client.websocket import websocket_client
    except ImportError:
        raise ImportError(
            "Could not import websocket_client. ",
            "To use Websocket connections, please install the required dependency with: ",
            "'pip install mcp[ws]' or 'pip install websockets'",
        ) from None

    async with websocket_client(url) as (read, write):
        async with ClientSession(read, write, **(session_kwargs or {})) as session:
            yield session 