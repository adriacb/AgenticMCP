import pytest
from unittest.mock import AsyncMock, patch
import httpx
from mcpagent.infrastructure.external.mcp.sse import create_sse_session
from mcp.client.session import ClientSession
from mcpagent.infrastructure.external.mcp.sse import (
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT,
)

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
def mock_sse_client():
    # Create mock streams with basic behavior
    read_stream = AsyncMock()
    read_stream.read = AsyncMock(return_value=b"")
    write_stream = AsyncMock()
    write_stream.write = AsyncMock()
    
    # Create the SSE client mock that returns a tuple of streams
    mock = AsyncMock()
    mock.return_value = mock  # Make the mock return itself
    mock.__aenter__.return_value = (read_stream, write_stream)
    mock.__aexit__.return_value = None
    
    # Patch the sse_client at the correct import path
    with patch("mcpagent.infrastructure.external.mcp.sse.sse_client", return_value=mock) as patched:
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
    with patch("mcpagent.infrastructure.external.mcp.sse.ClientSession", return_value=session) as patched:
        yield patched

@pytest.mark.asyncio
async def test_create_sse_session(mock_httpx_client_factory, mock_sse_client, mock_client_session):
    # Arrange
    url = "http://example.com/sse"
    headers = {"Authorization": "Bearer token"}
    timeout = 1.0
    sse_read_timeout = 1.0

    # Act
    async with create_sse_session(
        url=url,
        headers=headers,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
        httpx_client_factory=mock_httpx_client_factory,
    ) as session:
        # Assert
        assert isinstance(session, ClientSession)
        
        # Verify SSE client was called correctly
        mock_sse_client.assert_called_once_with(
            url,
            headers,
            timeout,
            sse_read_timeout,
            httpx_client_factory=mock_httpx_client_factory,
        )
        
        # Verify ClientSession was created with the streams
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2  # read, write
        assert call_args[0] == mock_sse_client.return_value.__aenter__.return_value[0]  # read stream
        assert call_args[1] == mock_sse_client.return_value.__aenter__.return_value[1]  # write stream

@pytest.mark.asyncio
async def test_create_sse_session_with_defaults(mock_httpx_client_factory, mock_sse_client, mock_client_session):
    # Arrange
    url = "http://example.com/sse"

    # Act
    async with create_sse_session(
        url=url,
        httpx_client_factory=mock_httpx_client_factory,
    ) as session:
        # Assert
        assert isinstance(session, ClientSession)
        
        # Verify SSE client was called with defaults
        mock_sse_client.assert_called_once_with(
            url,
            None,
            DEFAULT_HTTP_TIMEOUT,
            DEFAULT_SSE_READ_TIMEOUT,
            httpx_client_factory=mock_httpx_client_factory,
        )
        
        # Verify ClientSession was created with the streams
        mock_client_session.assert_called_once()
        call_args = mock_client_session.call_args[0]
        assert len(call_args) == 2  # read, write
        assert call_args[0] == mock_sse_client.return_value.__aenter__.return_value[0]  # read stream
        assert call_args[1] == mock_sse_client.return_value.__aenter__.return_value[1]  # write stream

@pytest.mark.asyncio
async def test_create_sse_session_missing_httpx():
    with patch.dict("sys.modules", {"httpx": None}):
        with pytest.raises(ModuleNotFoundError, match="import of httpx halted; None in sys.modules"):
            async with create_sse_session(url="http://example.com/sse"):
                pass

@pytest.mark.asyncio
async def test_create_sse_session_stream_error(mock_sse_client):
    # Arrange
    url = "http://example.com/sse"
    headers = {"Authorization": "Bearer token"}
    mock_sse_client.side_effect = Exception("Stream error")

    # Act & Assert
    with pytest.raises(Exception, match="Stream error"):
        async with create_sse_session(url=url, headers=headers):
            pass 