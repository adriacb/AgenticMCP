from typing import List

from mcpagent.core.domain.entities.llm import ChatLLM
from mcpagent.core.domain.value_objects import AgentConfig
from mcpagent.core.domain.interfaces import AgentInterface, ToolRegistryInterface, BaseMessage

class Agent(AgentInterface):
    def __init__(self, config: AgentConfig, tool_registry: ToolRegistryInterface=None):
        self.config = config
        self.tool_registry = tool_registry
        self.llm = self._init_llm()

    def _init_llm(self) -> ChatLLM:
        # Initialize the LLM with the provided configuration
        return ChatLLM(llm_config=self.config.llm_config, tool_registry=self.tool_registry)

    def invoke(self, input: List[BaseMessage]) -> str:
        return self.llm.invoke(input)
    
    async def ainvoke(self, input: List[BaseMessage]) -> str:
        return await self.llm.ainvoke(input)
    
    def __repr__(self):
        return f"AgentCard(name={self.config.agent_card.name}, description={self.config.agent_card.description}, has_tools={self.tool_registry is not None})"