from typing import Any, AsyncIterator, Optional, Protocol
from contextlib import asynccontextmanager
import httpx
from mcp import ClientSession
from mcp.client.sse import sse_client

DEFAULT_HTTP_TIMEOUT = 5
DEFAULT_SSE_READ_TIMEOUT = 60 * 5

class McpHttpClientFactory(Protocol):
    def __call__(
        self,
        headers: dict[str, str] | None = None,
        timeout: httpx.Timeout | None = None,
        auth: httpx.Auth | None = None,
    ) -> httpx.AsyncClient: ...

@asynccontextmanager
async def create_sse_session(
    url: str,
    headers: Optional[dict[str, Any]] = None,
    timeout: float = DEFAULT_HTTP_TIMEOUT,
    sse_read_timeout: float = DEFAULT_SSE_READ_TIMEOUT,
    session_kwargs: Optional[dict[str, Any]] = None,
    httpx_client_factory: Optional[McpHttpClientFactory] = None,
) -> AsyncIterator[ClientSession]:
    """Create a new session to an MCP server using SSE

    Args:
        url: URL of the SSE server
        headers: HTTP headers to send to the SSE endpoint
        timeout: HTTP timeout
        sse_read_timeout: SSE read timeout
        session_kwargs: Additional keyword arguments to pass to the ClientSession
        httpx_client_factory: Custom factory for httpx.AsyncClient (optional)
    """
    # Create and store the connection
    kwargs = {}
    if httpx_client_factory is not None:
        kwargs["httpx_client_factory"] = httpx_client_factory

    async with sse_client(url, headers, timeout, sse_read_timeout, **kwargs) as (read, write):
        async with ClientSession(read, write, **(session_kwargs or {})) as session:
            yield session 