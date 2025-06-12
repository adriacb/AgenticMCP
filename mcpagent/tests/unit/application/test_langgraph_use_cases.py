import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from mcpagent.application.langgraph_use_cases import (
    generate_response,
    generate_stream,
    handle_websocket
)

@pytest.mark.asyncio
async def test_generate_response():
    """Test non-streaming response generation."""
    test_messages = [HumanMessage(content="Hello")]
    mock_response = AIMessage(content="Hi there!")
    
    with patch("mcpagent.application.langgraph_use_cases.graph") as mock_graph:
        mock_graph.ainvoke = AsyncMock(return_value={
            "messages": test_messages + [mock_response],
            "next": "end"
        })
        
        result = await generate_response(test_messages)
        
        assert result["messages"] == test_messages + [mock_response]
        assert result["next"] == "end"

@pytest.mark.asyncio
async def test_generate_stream():
    """Test streaming response generation."""
    test_messages = [HumanMessage(content="Hello")]
    mock_events = [
        {"messages": test_messages + [AIMessage(content="Hi")]},
        {"messages": test_messages + [AIMessage(content="Hi there")]},
        {"messages": test_messages + [AIMessage(content="Hi there!")]}
    ]
    
    with patch("mcpagent.application.langgraph_use_cases.graph") as mock_graph:
        mock_graph.astream = AsyncMock(return_value=mock_events)
        
        events = []
        async for event in generate_stream(test_messages):
            events.append(event)
        
        assert len(events) == 3
        assert events == mock_events

@pytest.mark.asyncio
async def test_handle_websocket():
    """Test WebSocket handler."""
    mock_websocket = AsyncMock()
    test_messages = [HumanMessage(content="Hello")]
    mock_events = [
        {"messages": test_messages + [AIMessage(content="Hi")]},
        {"messages": test_messages + [AIMessage(content="Hi there")]},
        {"messages": test_messages + [AIMessage(content="Hi there!")]}
    ]
    
    with patch("mcpagent.application.langgraph_use_cases.generate_stream") as mock_stream:
        mock_stream.return_value = mock_events
        
        await handle_websocket(mock_websocket, test_messages)
        
        mock_websocket.accept.assert_called_once()
        assert mock_websocket.send_json.call_count == 3
        mock_websocket.close.assert_called_once() 