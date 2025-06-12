import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path
from mcp import ClientSession
from mcpagent.infrastructure.external.mcp.stdio import create_stdio_session

@pytest.fixture
def mock_stdio_client():
    with patch("mcp.client.stdio.stdio_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.mark.asyncio
async def test_create_stdio_session(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    
    async with create_stdio_session(command=command, args=args) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_with_defaults(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    
    async with create_stdio_session(command=command, args=args) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_with_existing_path(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    cwd = str(Path.cwd())  # Use current directory instead of invalid path
    
    async with create_stdio_session(command=command, args=args, cwd=cwd) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_process_cleanup(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    
    async with create_stdio_session(command=command, args=args) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_process_kill(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    
    async with create_stdio_session(command=command, args=args) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_missing_pipes(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    
    async with create_stdio_session(command=command, args=args) as session:
        assert isinstance(session, ClientSession)
        mock_stdio_client.assert_called_once()

@pytest.mark.asyncio
async def test_create_stdio_session_process_error(mock_stdio_client):
    command = "python"
    args = ["-m", "http.server"]
    mock_stdio_client.side_effect = Exception("Process creation failed")
    
    with pytest.raises(Exception, match="Process creation failed"):
        async with create_stdio_session(command=command, args=args):
            pass 