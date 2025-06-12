import pytest
from unittest.mock import AsyncMock

from mcpagent.application.use_cases.mcp import LoadMCPResourcesUseCase
from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.resource_loader import ResourceLoader

@pytest.fixture
def mock_resource_loader():
    return AsyncMock(spec=ResourceLoader)

@pytest.fixture
def mock_session():
    session = AsyncMock(spec=Session)
    session.is_active.return_value = True
    return session

@pytest.fixture
def load_resources_use_case(mock_resource_loader):
    return LoadMCPResourcesUseCase(mock_resource_loader)

@pytest.mark.asyncio
async def test_execute_with_single_uri(load_resources_use_case, mock_resource_loader, mock_session):
    # Arrange
    uri = "test/resource"
    expected_resources = [{"uri": uri, "content": "test"}]
    mock_resource_loader.load_resources.return_value = expected_resources
    
    # Act
    result = await load_resources_use_case.execute(
        session=mock_session,
        uris=[uri],
    )
    
    # Assert
    assert result == expected_resources
    mock_resource_loader.load_resources.assert_called_once_with(
        session=mock_session,
        uris=[uri],
    )

@pytest.mark.asyncio
async def test_execute_with_multiple_uris(load_resources_use_case, mock_resource_loader, mock_session):
    # Arrange
    uris = ["test/resource1", "test/resource2"]
    expected_resources = [
        {"uri": uris[0], "content": "test1"},
        {"uri": uris[1], "content": "test2"},
    ]
    mock_resource_loader.load_resources.return_value = expected_resources
    
    # Act
    result = await load_resources_use_case.execute(
        session=mock_session,
        uris=uris,
    )
    
    # Assert
    assert result == expected_resources
    mock_resource_loader.load_resources.assert_called_once_with(
        session=mock_session,
        uris=uris,
    )

@pytest.mark.asyncio
async def test_execute_with_no_uris(load_resources_use_case, mock_resource_loader, mock_session):
    # Arrange
    expected_resources = [
        {"uri": "test/resource1", "content": "test1"},
        {"uri": "test/resource2", "content": "test2"},
    ]
    mock_resource_loader.load_resources.return_value = expected_resources
    
    # Act
    result = await load_resources_use_case.execute(session=mock_session)
    
    # Assert
    assert result == expected_resources
    mock_resource_loader.load_resources.assert_called_once_with(
        session=mock_session,
        uris=None,
    )

@pytest.mark.asyncio
async def test_execute_with_inactive_session(load_resources_use_case, mock_session):
    # Arrange
    mock_session.is_active.return_value = False
    
    # Act & Assert
    with pytest.raises(ValueError, match="Session is not active"):
        await load_resources_use_case.execute(session=mock_session) 