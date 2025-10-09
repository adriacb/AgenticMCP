import pytest

from mcpagent.core.domain.value_objects import AgentConfig, LLMConfig, AgentCard


# create dummy data for testing
@pytest.fixture
def dummy_llm_config():
    return LLMConfig(model="gpt-4", temperature=0.5)


@pytest.fixture
def dummy_agent_card():
    return AgentCard(name="TestAgent", description="An agent that assists with tasks.")


@pytest.fixture
def dummy_agent_config(dummy_llm_config, dummy_agent_card):
    return AgentConfig(
        llm_config=dummy_llm_config,
        agent_card=dummy_agent_card,
        system_prompt="You are a helpful assistant.",
    )


def test_agent_config_creation(dummy_agent_config):
    assert dummy_agent_config.llm_config.model == "gpt-4"
    assert dummy_agent_config.llm_config.temperature == 0.5
    assert dummy_agent_config.agent_card.name == "TestAgent"
    assert (
        dummy_agent_config.agent_card.description == "An agent that assists with tasks."
    )
    assert dummy_agent_config.system_prompt == "You are a helpful assistant."


def test_agent_config_defaults():
    default_config = AgentConfig(llm_config=LLMConfig(model="gpt-3.5"))
    assert default_config.agent_card.name == "Default Assistant"
    assert default_config.agent_card.description == "A default assistant configuration."
    assert default_config.system_prompt == "You are a helpful assistant."


def test_agent_card_creation():
    card = AgentCard(name="TestAgent", description="An agent that assists with tasks.")
    assert card.name == "TestAgent"
    assert card.description == "An agent that assists with tasks."
    assert card.version == "1.0.0"  # Default value
    assert isinstance(card.skills, list)  # Default to an empty list
    assert len(card.skills) == 0  # Ensure skills list is empty by default
