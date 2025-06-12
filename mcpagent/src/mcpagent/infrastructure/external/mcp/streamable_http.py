from typing import Any, AsyncIterator, Optional, Protocol, TYPE_CHECKING
from contextlib import asynccontextmanager
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

DEFAULT_STREAMABLE_HTTP_TIMEOUT = timedelta(seconds=30)
DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT = timedelta(seconds=60 * 5)

if TYPE_CHECKING:
    import httpx

class McpHttpClientFactory(Protocol):
    def __call__(
        self,
        headers: dict[str, str] | None = None,
        timeout: "httpx.Timeout | None" = None,
        auth: "httpx.Auth | None" = None,
    ) -> "httpx.AsyncClient": ...

@asynccontextmanager
async def create_streamable_http_session(
    url: str,
    headers: Optional[dict[str, Any]] = None,
    timeout: timedelta = DEFAULT_STREAMABLE_HTTP_TIMEOUT,
    sse_read_timeout: timedelta = DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
    terminate_on_close: bool = True,
    session_kwargs: Optional[dict[str, Any]] = None,
    httpx_client_factory: Optional[McpHttpClientFactory] = None,
):
    """Create a new session to an MCP server using Streamable HTTP

    Args:
        url: URL of the endpoint to connect to
        headers: HTTP headers to send to the endpoint
        timeout: HTTP timeout
        sse_read_timeout: How long (in seconds) the client will wait for a new event before disconnecting.
        terminate_on_close: Whether to terminate the session on close
        session_kwargs: Additional keyword arguments to pass to the ClientSession
        httpx_client_factory: Custom factory for httpx.AsyncClient (optional)
    """
    # Import httpx here for patching in tests
    import httpx
    # Create and store the connection
    kwargs = {}
    if httpx_client_factory is not None:
        kwargs["httpx_client_factory"] = httpx_client_factory

    async with streamablehttp_client(
        url, headers, timeout, sse_read_timeout, terminate_on_close, **kwargs
    ) as (read, write, _):
        async with ClientSession(read, write, **(session_kwargs or {})) as session:
            yield session 