import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from mcpagent.infrastructure.external.mcp.session_factory import create_session
from mcp.client.session import ClientSession
from mcpagent.domain.interfaces.connection import (
    StreamableHttpConnection,
    SSEConnection,
    StdioConnection,
    WebsocketConnection,
)
from mcpagent.infrastructure.external.mcp.session_factory import (
    DEFAULT_STREAMABLE_HTTP_TIMEOUT,
    DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT,
)

@pytest.fixture(autouse=True)
def mock_clients():
    with patch("mcp.client.sse.sse_client") as sse_mock, \
         patch("mcp.client.streamable_http.streamablehttp_client") as streamable_mock, \
         patch("mcp.client.stdio.stdio_client") as stdio_mock, \
         patch("mcp.client.websocket.websocket_client") as websocket_mock:
        sse_mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        streamable_mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock(), None)
        stdio_mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        websocket_mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield {
            "sse": sse_mock,
            "streamable": streamable_mock,
            "stdio": stdio_mock,
            "websocket": websocket_mock,
        }

@pytest.fixture
def mock_httpx_client():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.__aenter__.return_value = client
    client.__aexit__.return_value = None
    return client

@pytest.fixture
def mock_httpx_client_factory(mock_httpx_client):
    def factory(**kwargs):
        return mock_httpx_client
    return factory

@pytest.fixture
def mock_streamablehttp_client():
    with patch("mcp.client.streamable_http.streamablehttp_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock(), None)
        yield mock

@pytest.fixture
def mock_sse_client():
    with patch("mcp.client.sse.sse_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.fixture
def mock_stdio_client():
    with patch("mcp.client.stdio.stdio_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.fixture
def mock_websocket_client():
    with patch("mcp.client.websocket.websocket_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.mark.asyncio
async def test_create_streamable_http_session(mock_streamablehttp_client):
    connection: StreamableHttpConnection = {
        "transport": "streamable_http",
        "url": "http://example.com/stream",
        "headers": {"Authorization": "Bearer token"},
        "timeout": timedelta(seconds=10),
        "sse_read_timeout": timedelta(seconds=120),
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            "http://example.com/stream",
            {"Authorization": "Bearer token"},
            timedelta(seconds=10),
            timedelta(seconds=120),
            True,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_with_defaults(mock_streamablehttp_client):
    connection: StreamableHttpConnection = {
        "transport": "streamable_http",
        "url": "http://example.com/stream",
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            "http://example.com/stream",
            None,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            True,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_missing_url():
    with pytest.raises(ValueError, match="'url' parameter is required for Streamable HTTP connection"):
        async with create_session({"transport": "streamable_http"}):  # type: ignore
            pass

@pytest.mark.asyncio
async def test_create_sse_session(mock_sse_client):
    connection: SSEConnection = {
        "transport": "sse",
        "url": "http://example.com/sse",
        "headers": {"Authorization": "Bearer token"},
        "timeout": 10.0,
        "sse_read_timeout": 120.0,
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_sse_client.assert_called_once_with(
            "http://example.com/sse",
            {"Authorization": "Bearer token"},
            10.0,
            120.0,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_sse_session_with_defaults(mock_sse_client):
    connection: SSEConnection = {
        "transport": "sse",
        "url": "http://example.com/sse",
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_sse_client.assert_called_once_with(
            "http://example.com/sse",
            None,
            DEFAULT_HTTP_TIMEOUT,
            DEFAULT_SSE_READ_TIMEOUT,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_sse_session_missing_url():
    with pytest.raises(ValueError, match="'url' parameter is required for SSE connection"):
        async with create_session({"transport": "sse"}):  # type: ignore
            pass

@pytest.mark.asyncio
async def test_create_stdio_session(mock_stdio_client):
    connection: StdioConnection = {
        "transport": "stdio",
        "command": "python",
        "args": ["-c", "print('Hello')"],
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_with_defaults(mock_stdio_client):
    connection: StdioConnection = {
        "transport": "stdio",
        "command": "python",
        "args": ["-c", "print('Hello')"],
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_missing_command():
    with pytest.raises(ValueError, match="'command' parameter is required for stdio connection"):
        async with create_session({"transport": "stdio", "args": ["-c", "print('Hello')"]}):  # type: ignore
            pass

@pytest.mark.asyncio
async def test_create_stdio_session_missing_args():
    with pytest.raises(ValueError, match="'args' parameter is required for stdio connection"):
        async with create_session({"transport": "stdio", "command": "python"}):  # type: ignore
            pass

@pytest.mark.asyncio
async def test_create_websocket_session(mock_websocket_client):
    connection: WebsocketConnection = {
        "transport": "websocket",
        "url": "ws://example.com/ws",
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_websocket_client.assert_called_once_with(
            "ws://example.com/ws",
        )

@pytest.mark.asyncio
async def test_create_websocket_session_with_defaults(mock_websocket_client):
    connection: WebsocketConnection = {
        "transport": "websocket",
        "url": "ws://example.com/ws",
    }
    
    async with create_session(connection) as session:
        assert isinstance(session, ClientSession)
        mock_websocket_client.assert_called_once_with(
            "ws://example.com/ws",
        )

@pytest.mark.asyncio
async def test_create_websocket_session_missing_url():
    with pytest.raises(ValueError, match="'url' parameter is required for Websocket connection"):
        async with create_session({"transport": "websocket"}):  # type: ignore
            pass

@pytest.mark.asyncio
async def test_create_websocket_session_missing_websockets():
    with patch("mcp.client.websocket.websocket_client", side_effect=ImportError("Could not import websocket_client")):
        with pytest.raises(ImportError, match="Could not import websocket_client"):
            async with create_session({"transport": "websocket", "url": "ws://example.com/ws"}):  # type: ignore
                pass 