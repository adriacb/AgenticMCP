from typing import Any, Literal, TypedDict, Protocol
from pathlib import Path
from datetime import timedelta
import httpx

class McpHttpClientFactory(Protocol):
    """Protocol for HTTP client factory."""
    def __call__(
        self,
        headers: dict[str, str] | None = None,
        timeout: httpx.Timeout | None = None,
        auth: httpx.Auth | None = None,
    ) -> httpx.AsyncClient: ...

class Connection(TypedDict):
    """Base connection interface."""
    transport: Literal["stdio", "sse", "streamable_http", "websocket"]

class StdioConnection(TypedDict):
    """Stdio connection configuration."""
    transport: Literal["stdio"]
    command: str
    args: list[str]
    env: dict[str, str] | None
    cwd: str | Path | None
    encoding: str
    encoding_error_handler: Literal["strict", "ignore", "replace"]
    session_kwargs: dict[str, Any] | None

class SSEConnection(TypedDict):
    """SSE connection configuration."""
    transport: Literal["sse"]   
    url: str
    headers: dict[str, Any] | None
    timeout: float
    sse_read_timeout: float
    session_kwargs: dict[str, Any] | None
    httpx_client_factory: McpHttpClientFactory | None

class StreamableHttpConnection(TypedDict):
    """Streamable HTTP connection configuration."""
    transport: Literal["streamable_http"]
    url: str
    headers: dict[str, Any] | None
    timeout: timedelta
    sse_read_timeout: timedelta
    terminate_on_close: bool
    session_kwargs: dict[str, Any] | None
    httpx_client_factory: McpHttpClientFactory | None

class WebsocketConnection(TypedDict):
    """Websocket connection configuration."""
    transport: Literal["websocket"]
    url: str
    session_kwargs: dict[str, Any] | None

Connection = StdioConnection | SSEConnection | StreamableHttpConnection | WebsocketConnection 