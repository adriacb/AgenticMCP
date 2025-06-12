from typing import List
from mcpagent.domain.interfaces.agent import AgentInterface
from mcpagent.domain.interfaces.llm import LLMInterface
from mcpagent.domain.entities.tools import Tool

class MCPAgent(AgentInterface):
    def __init__(self, 
                 tools: List[Tool]|None=None,
                 llm: LLMInterface|None=None,
                 prompt: str|None=None,
                 ):
        self.tools = tools
        self.llm = llm
