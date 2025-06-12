import pytest
from unittest.mock import AsyncMock

from mcpagent.application.use_cases.mcp import LoadMCPToolsUseCase
from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.tool_loader import ToolLoader

@pytest.fixture
def mock_tool_loader():
    return AsyncMock(spec=ToolLoader)

@pytest.fixture
def mock_session():
    session = AsyncMock(spec=Session)
    session.is_active.return_value = True
    return session

@pytest.fixture
def load_tools_use_case(mock_tool_loader):
    return LoadMCPToolsUseCase(mock_tool_loader)

@pytest.mark.asyncio
async def test_execute_with_session(load_tools_use_case, mock_tool_loader, mock_session):
    # Arrange
    expected_tools = [{"name": "test_tool"}]
    mock_tool_loader.load_tools.return_value = expected_tools
    
    # Act
    result = await load_tools_use_case.execute(session=mock_session)
    
    # Assert
    assert result == expected_tools
    mock_tool_loader.load_tools.assert_called_once_with(session=mock_session)

@pytest.mark.asyncio
async def test_execute_with_inactive_session(load_tools_use_case, mock_session):
    # Arrange
    mock_session.is_active.return_value = False
    
    # Act & Assert
    with pytest.raises(ValueError, match="Session is not active"):
        await load_tools_use_case.execute(session=mock_session) 