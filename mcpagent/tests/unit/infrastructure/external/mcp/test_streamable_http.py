import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from mcpagent.infrastructure.external.mcp.streamable_http import create_streamable_http_session, DEFAULT_STREAMABLE_HTTP_TIMEOUT, DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT
from mcp.client.session import ClientSession

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
    # Create mock streams with basic behavior
    read_stream = AsyncMock()
    read_stream.read = AsyncMock(return_value=b"")
    write_stream = AsyncMock()
    write_stream.write = AsyncMock()
    extra = AsyncMock()
    
    # Create the streamablehttp_client mock that returns a tuple of streams
    mock = AsyncMock()
    mock.return_value = mock
    mock.__aenter__.return_value = (read_stream, write_stream, extra)
    mock.__aexit__.return_value = None
    
    # Patch the streamablehttp_client at the correct import path
    with patch("mcpagent.infrastructure.external.mcp.streamable_http.streamablehttp_client", return_value=mock) as patched:
        yield patched

@pytest.fixture
def mock_client_session():
    # Create a ClientSession mock with basic behavior
    session = AsyncMock(spec=ClientSession)
    session.__aenter__.return_value = session
    session.__aexit__.return_value = None
    session.run = AsyncMock()
    session.send = AsyncMock()
    session.receive = AsyncMock(return_value=None)
    
    # Patch the ClientSession at the correct import path
    with patch("mcpagent.infrastructure.external.mcp.streamable_http.ClientSession", return_value=session) as patched:
        yield patched

@pytest.mark.asyncio
async def test_create_streamable_http_session(mock_httpx_client_factory, mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    timeout = 1.0
    sse_read_timeout = 1.0
    terminate_on_close = True

    async with create_streamable_http_session(
        url=url,
        headers=headers,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
        terminate_on_close=terminate_on_close,
        httpx_client_factory=mock_httpx_client_factory,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            timeout,
            sse_read_timeout,
            terminate_on_close,
            httpx_client_factory=mock_httpx_client_factory,
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2  # read, write
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_with_defaults(mock_httpx_client_factory, mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    async with create_streamable_http_session(
        url=url,
        httpx_client_factory=mock_httpx_client_factory,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            True,
            httpx_client_factory=mock_httpx_client_factory,
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_with_custom_client_factory(mock_httpx_client_factory, mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    headers = {"Authorization": "Bearer token"}
    async with create_streamable_http_session(
        url=url,
        headers=headers,
        httpx_client_factory=mock_httpx_client_factory,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            headers,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            True,
            httpx_client_factory=mock_httpx_client_factory,
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_without_factory(mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    async with create_streamable_http_session(url=url) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            True
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_termination(mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    async with create_streamable_http_session(url=url, terminate_on_close=False) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            False
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_no_termination(mock_streamablehttp_client, mock_client_session):
    url = "http://example.com/stream"
    async with create_streamable_http_session(url=url, terminate_on_close=True) as session:
        assert isinstance(session, ClientSession)
        mock_streamablehttp_client.assert_called_once_with(
            url,
            None,
            DEFAULT_STREAMABLE_HTTP_TIMEOUT,
            DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT,
            True
        )
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2
        assert call_args[0] == mock_streamablehttp_client.return_value.__aenter__.return_value[0]
        assert call_args[1] == mock_streamablehttp_client.return_value.__aenter__.return_value[1]

@pytest.mark.asyncio
async def test_create_streamable_http_session_missing_httpx():
    with patch.dict("sys.modules", {"httpx": None}):
        with pytest.raises(ModuleNotFoundError, match="import of httpx halted; None in sys.modules"):
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