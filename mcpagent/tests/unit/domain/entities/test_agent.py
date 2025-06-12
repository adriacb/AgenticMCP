import pytest
from mcpagent.domain.entities.agent import Agent

class TestAgent(Agent):
    """Concrete implementation of Agent for testing purposes."""
    
    def __init__(self):
        self.last_input = None
        self.last_experience = None
    
    async def process(self, input_data: any) -> any:
        self.last_input = input_data
        return f"Processed: {input_data}"
    
    async def learn(self, experience: dict[str, any]) -> None:
        self.last_experience = experience

@pytest.mark.asyncio
async def test_agent_process():
    """Test that the agent can process input correctly."""
    agent = TestAgent()
    test_input = "test input"
    
    result = await agent.process(test_input)
    
    assert agent.last_input == test_input
    assert result == f"Processed: {test_input}"

@pytest.mark.asyncio
async def test_agent_learn():
    """Test that the agent can learn from experience."""
    agent = TestAgent()
    test_experience = {
        "input": "test input",
        "action": "test action",
        "result": "test result",
        "reward": 1.0
    }
    
    await agent.learn(test_experience)
    
    assert agent.last_experience == test_experience

def test_agent_abstract_methods():
    """Test that Agent class is properly abstract."""
    with pytest.raises(TypeError):
        Agent()  # Should raise TypeError as Agent is abstract 