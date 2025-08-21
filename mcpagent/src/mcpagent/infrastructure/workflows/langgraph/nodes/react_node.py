from typing import List
from mcpagent.infrastructure.agents.react_agent import create_react_agent
from mcpagent.domain.interfaces.llm import LLMInterface
from mcpagent.domain.entities.agents.agent import Agent
from mcpagent.domain.entities.llm.openai import OpenAILLMClient
from mcpagent.application.services.config import OpenAILLMConfig

def react_node(
    tools: List,
    agent_config_path: str,
    ) -> Agent:

    openai_config = OpenAILLMConfig.from_env_file(agent_config_path)

    return create_react_agent(
        llm = OpenAILLMClient(
            openai_config
            ),
        tools = tools
        )