import pytest
from unittest.mock import AsyncMock, patch
from datetime import timedelta
from mcp import ClientSession
from mcpagent.infrastructure.external.mcp.sse import (
    create_sse_session,
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT,
)

@pytest.fixture
def mock_sse_client():
    with patch("mcp.client.sse.sse_client") as mock:
        mock.return_value.__aenter__.return_value = (AsyncMock(), AsyncMock())
        yield mock

@pytest.mark.asyncio
async def test_create_sse_session(mock_sse_client):
    url = "http://example.com/sse"
    headers = {"Authorization": "Bearer token"}
    timeout = timedelta(seconds=10)
    sse_read_timeout = timedelta(seconds=120)
    
    async with create_sse_session(
        url=url,
        headers=headers,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_sse_client.assert_called_once_with(
            url,
            headers,
            timeout,
            sse_read_timeout,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_sse_session_with_defaults(mock_sse_client):
    url = "http://example.com/sse"
    
    async with create_sse_session(url=url) as session:
        assert isinstance(session, ClientSession)
        mock_sse_client.assert_called_once_with(
            url,
            None,
            None,
            None,
            httpx_client_factory=None,
        )

@pytest.mark.asyncio
async def test_create_sse_session_with_custom_client_factory(mock_sse_client):
    url = "http://example.com/sse"
    headers = {"Authorization": "Bearer token"}
    
    async def client_factory(**kwargs):
        return AsyncMock()
    
    async with create_sse_session(
        url=url,
        headers=headers,
        httpx_client_factory=client_factory,
    ) as session:
        assert isinstance(session, ClientSession)
        mock_sse_client.assert_called_once_with(
            url,
            headers,
            None,
            None,
            httpx_client_factory=client_factory,
        ) 