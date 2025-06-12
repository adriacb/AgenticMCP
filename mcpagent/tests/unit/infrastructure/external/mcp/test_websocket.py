import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, patch, MagicMock
import websockets
from mcp.client.session import ClientSession as MCPClientSession
from mcpagent.infrastructure.external.mcp.websocket import create_websocket_session

@pytest.fixture
def mock_websocket():
    ws = AsyncMock(spec=websockets.WebSocketClientProtocol)
    ws.__aenter__.return_value = ws
    ws.__aexit__.return_value = None
    ws.recv = AsyncMock()
    ws.send = AsyncMock()
    ws.close = AsyncMock()
    return ws

@pytest.fixture
def mock_websocket_connect():
    with patch("websockets.connect") as mock_connect:
        mock_connect.return_value = AsyncMock()
        yield mock_connect

@pytest.fixture
def mock_websocket_client():
    with patch("mcp.client.websocket.websocket_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.mark.asyncio
async def test_create_websocket_session(mock_websocket_client):
    url = "ws://example.com/ws"
    
    async with create_websocket_session(url=url) as session:
        assert isinstance(session, MCPClientSession)
        mock_websocket_client.assert_called_once_with(url)

@pytest.mark.asyncio
async def test_create_websocket_session_with_defaults(mock_websocket_client):
    url = "ws://example.com/ws"
    
    async with create_websocket_session(url=url) as session:
        assert isinstance(session, MCPClientSession)
        mock_websocket_client.assert_called_once_with(url)

@pytest.mark.asyncio
async def test_create_websocket_session_missing_websockets():
    with patch("mcp.client.websocket.websocket_client", side_effect=ImportError("Could not import websocket_client")):
        with pytest.raises(ImportError, match="Could not import websocket_client"):
            async with create_websocket_session(url="ws://example.com/ws"):
                pass

@pytest.mark.asyncio
async def test_create_websocket_session_connection_error(mock_websocket_client):
    url = "ws://example.com/ws"
    mock_websocket_client.side_effect = websockets.exceptions.WebSocketException("Connection failed")
    
    with pytest.raises(websockets.exceptions.WebSocketException, match="Connection failed"):
        async with create_websocket_session(url=url):
            pass

@pytest.mark.asyncio
async def test_create_websocket_session_termination(mock_websocket_client):
    url = "ws://example.com/ws"
    
    async with create_websocket_session(url=url) as session:
        assert isinstance(session, MCPClientSession)
        mock_websocket_client.assert_called_once_with(url)

@pytest.mark.asyncio
async def test_create_websocket_session_no_termination(mock_websocket_client):
    url = "ws://example.com/ws"
    
    async with create_websocket_session(url=url) as session:
        assert isinstance(session, MCPClientSession)
        mock_websocket_client.assert_called_once_with(url) 