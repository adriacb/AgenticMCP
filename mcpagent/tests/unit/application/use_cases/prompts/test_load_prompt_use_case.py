import pytest
from unittest.mock import AsyncMock

from mcpagent.application.use_cases.mcp import LoadMCPPromptUseCase
from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.prompt_loader import PromptLoader

@pytest.fixture
def mock_prompt_loader():
    return AsyncMock(spec=PromptLoader)

@pytest.fixture
def mock_session():
    session = AsyncMock(spec=Session)
    session.is_active.return_value = True
    session.reset_mock()  # Reset the mock before each test
    return session

@pytest.fixture
def load_prompt_use_case(mock_prompt_loader):
    return LoadMCPPromptUseCase(mock_prompt_loader)

@pytest.mark.asyncio
async def test_execute_success(load_prompt_use_case, mock_prompt_loader, mock_session):
    # Arrange
    expected_prompt = "test prompt"
    mock_prompt_loader.load_prompt.return_value = expected_prompt
    
    # Act
    result = await load_prompt_use_case.execute(
        session=mock_session,
        name="test_prompt",
        arguments={"key": "value"}
    )
    
    # Assert
    assert result == expected_prompt
    mock_prompt_loader.load_prompt.assert_called_once_with(
        session=mock_session,
        name="test_prompt",
        arguments={"key": "value"}
    )

@pytest.mark.asyncio
async def test_execute_with_inactive_session(load_prompt_use_case, mock_session):
    # Arrange
    mock_session.is_active.return_value = False
    
    # Act & Assert
    with pytest.raises(ValueError, match="Session is not active"):
        await load_prompt_use_case.execute(
            session=mock_session,
            name="test_prompt"
        ) 