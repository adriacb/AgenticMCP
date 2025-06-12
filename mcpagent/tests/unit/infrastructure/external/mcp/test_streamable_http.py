import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from mcpagent.infrastructure.external.mcp.streamable_http import create_streamable_http_session
from mcpagent.infrastructure.external.mcp.client_session import ClientSession
from mcp import ClientSession as MCPClientSession
from mcpagent.infrastructure.external.mcp.streamable_http import (
    DEFAULT_STREAMABLE_HTTP_TIMEOUT,
    DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
)

@pytest.fixture
def mock_httpx_client():
    client = AsyncMock(spec=httpx.AsyncClient)
    # Patch stream to be an async function returning a context manager
    class MockStreamContext:
        async def __aenter__(self):
            class MockStream:
                async def aiter_bytes(self):
                    yield b"data"
                async def aclose(self):
                    pass
            return MockStream()
        async def __aexit__(self, exc_type, exc, tb):
            pass
    client.stream = AsyncMock(return_value=MockStreamContext())
    client.request = AsyncMock()
    client.aclose = AsyncMock()
    return client

@pytest.fixture
def mock_httpx_client_factory(mock_httpx_client):
    async def factory():
        return mock_httpx_client
    return factory

@pytest.fixture
def mock_streamablehttp_client():
    with patch("mcp.client.streamable_http.streamablehttp_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock(), None)
        yield mock

@pytest.mark.asyncio
async def test_create_streamable_http_session(mock_streamablehttp_client):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    timeout = timedelta(seconds=10)
    sse_read_timeout = timedelta(seconds=120)
    
    async with create_streamable_http_session(
        url=url,
        headers=headers,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            timeout,
            sse_read_timeout,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_with_defaults(mock_streamablehttp_client):
    url = "http://example.com/stream"
    
    async with create_streamable_http_session(url=url) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            None,
            None,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_with_custom_client_factory(mock_streamablehttp_client):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    
    async def client_factory(**kwargs):
        return AsyncMock()
    
    async with create_streamable_http_session(
        url=url,
        headers=headers,
        httpx_client_factory=client_factory,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            None,
            None,
            httpx_client_factory=client_factory,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_without_factory(mock_streamablehttp_client):
    url = "http://example.com/stream"
    
    async with create_streamable_http_session(url=url) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            None,
            None,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_termination(mock_streamablehttp_client):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    terminate_on_close = True
    
    async with create_streamable_http_session(
        url=url,
        headers=headers,
        terminate_on_close=terminate_on_close,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            None,
            None,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_no_termination(mock_streamablehttp_client):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    terminate_on_close = False
    
    async with create_streamable_http_session(
        url=url,
        headers=headers,
        terminate_on_close=terminate_on_close,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            None,
            None,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_streamable_http_session_missing_httpx():
    with patch.dict("sys.modules", {"httpx": None}):
        with pytest.raises(ImportError, match="Could not import httpx"):
            async with create_streamable_http_session(url="http://example.com/stream"):
                pass

@pytest.mark.asyncio
async def test_create_streamable_http_session_stream_error(mock_streamablehttp_client):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    mock_streamablehttp_client.side_effect = Exception("Stream error")
    
    with pytest.raises(Exception, match="Stream error"):
        async with create_streamable_http_session(url=url, headers=headers):
            pass 