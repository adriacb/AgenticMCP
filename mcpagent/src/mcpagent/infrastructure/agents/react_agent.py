from mcpagent.domain.entities.agents.agent import Agent
from mcpagent.domain.interfaces.llm import LLMInterface
from mcpagent.domain.entities.tools import Tool
from mcpagent.domain.interfaces.llm import OpenAILLMClient
from mcpagent.domain.interfaces.llm import OpenAILLMConfig
from typing import List, Any


def create_react_agent(
    llm: LLMInterface,
    tools: List[Tool],
    ) -> Agent:
        return Agent(
                llm=llm, 
                tools=tools, 
                prompt="You are a helpful assistant. Answer the following question as if you were a otaku: {question}"
                )

