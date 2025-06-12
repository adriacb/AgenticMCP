from typing import Any, AsyncIterator, Literal, Protocol, TypedDict
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
import httpx
from mcp import ClientSession

EncodingErrorHandler = Literal["strict", "ignore", "replace"]

DEFAULT_ENCODING = "utf-8"
DEFAULT_ENCODING_ERROR_HANDLER: EncodingErrorHandler = "strict"

DEFAULT_HTTP_TIMEOUT = 5
DEFAULT_SSE_READ_TIMEOUT = 60 * 5

DEFAULT_STREAMABLE_HTTP_TIMEOUT = timedelta(seconds=30)
DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT = timedelta(seconds=60 * 5)

class McpHttpClientFactory(Protocol):
    def __call__(
        self,
        headers: dict[str, str] | None = None,
        timeout: httpx.Timeout | None = None,
        auth: httpx.Auth | None = None,
    ) -> httpx.AsyncClient: ...

class StdioConnection(TypedDict):
    transport: Literal["stdio"]
    command: str
    args: list[str]
    env: dict[str, str] | None
    cwd: str | Path | None
    encoding: str
    encoding_error_handler: EncodingErrorHandler
    session_kwargs: dict[str, Any] | None

class SSEConnection(TypedDict):
    transport: Literal["sse"]
    url: str
    headers: dict[str, Any] | None
    timeout: float
    sse_read_timeout: float
    session_kwargs: dict[str, Any] | None
    httpx_client_factory: McpHttpClientFactory | None

class StreamableHttpConnection(TypedDict):
    transport: Literal["streamable_http"]
    url: str
    headers: dict[str, Any] | None
    timeout: timedelta
    sse_read_timeout: timedelta
    terminate_on_close: bool
    session_kwargs: dict[str, Any] | None
    httpx_client_factory: McpHttpClientFactory | None

class WebsocketConnection(TypedDict):
    transport: Literal["websocket"]
    url: str
    session_kwargs: dict[str, Any] | None

Connection = StdioConnection | SSEConnection | StreamableHttpConnection | WebsocketConnection

@asynccontextmanager
async def create_session(
    connection: Connection,
) -> AsyncIterator[ClientSession]:
    """Create a new session to an MCP server.

    Args:
        connection: Connection config to use to connect to the server

    Raises:
        ValueError: If transport is not recognized
        ValueError: If required parameters for the specified transport are missing

    Yields:
        A ClientSession
    """
    if "transport" not in connection:
        raise ValueError(
            "Configuration error: Missing 'transport' key in server configuration. "
            "Each server must include 'transport' with one of: "
            "'stdio', 'sse', 'websocket', 'streamable_http'. "
            "Please refer to the langchain-mcp-adapters documentation for more details."
        )

    transport = connection["transport"]
    if transport == "sse":
        if "url" not in connection:
            raise ValueError("'url' parameter is required for SSE connection")
        from mcp.client.sse import sse_client
        async with sse_client(
            connection["url"],
            connection.get("headers"),
            connection.get("timeout", DEFAULT_HTTP_TIMEOUT),
            connection.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT),
            httpx_client_factory=connection.get("httpx_client_factory"),
        ) as (read, write):
            async with ClientSession(read, write, **(connection.get("session_kwargs") or {})) as session:
                yield session
    elif transport == "streamable_http":
        if "url" not in connection:
            raise ValueError("'url' parameter is required for Streamable HTTP connection")
        from mcp.client.streamable_http import streamablehttp_client
        async with streamablehttp_client(
            connection["url"],
            connection.get("headers"),
            connection.get("timeout", DEFAULT_STREAMABLE_HTTP_TIMEOUT),
            connection.get("sse_read_timeout", DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT),
            connection.get("terminate_on_close", True),
            httpx_client_factory=connection.get("httpx_client_factory"),
        ) as (read, write, _):
            async with ClientSession(read, write, **(connection.get("session_kwargs") or {})) as session:
                yield session
    elif transport == "stdio":
        if "command" not in connection:
            raise ValueError("'command' parameter is required for stdio connection")
        if "args" not in connection:
            raise ValueError("'args' parameter is required for stdio connection")
        from mcp.client.stdio import stdio_client
        from mcp import StdioServerParameters
        server_params = StdioServerParameters(
            command=connection["command"],
            args=connection["args"],
            env=connection.get("env"),
            cwd=connection.get("cwd"),
            encoding=connection.get("encoding", DEFAULT_ENCODING),
            encoding_error_handler=connection.get("encoding_error_handler", DEFAULT_ENCODING_ERROR_HANDLER),
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write, **(connection.get("session_kwargs") or {})) as session:
                yield session
    elif transport == "websocket":
        if "url" not in connection:
            raise ValueError("'url' parameter is required for Websocket connection")
        try:
            from mcp.client.websocket import websocket_client
        except ImportError:
            raise ImportError(
                "Could not import websocket_client. ",
                "To use Websocket connections, please install the required dependency with: ",
                "'pip install mcp[ws]' or 'pip install websockets'",
            ) from None
        async with websocket_client(connection["url"]) as (read, write):
            async with ClientSession(read, write, **(connection.get("session_kwargs") or {})) as session:
                yield session
    else:
        raise ValueError(
            f"Unsupported transport: {transport}. "
            f"Must be one of: 'stdio', 'sse', 'websocket', 'streamable_http'"
        ) 