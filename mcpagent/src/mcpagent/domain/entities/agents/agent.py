from typing import Any, List, Generator, AsyncGenerator
from mcpagent.domain.interfaces.agent import AgentInterface
from mcpagent.domain.interfaces.llm import LLMInterface
from mcpagent.domain.entities.tools import Tool


class Agent(AgentInterface):
    def __init__(self, 
                 tools: List[Tool]|None=None,
                 llm: LLMInterface|None=None,
                 prompt: str|None=None,
                 ):
        self.tools = tools
        self.prompt = prompt
        self.llm = llm

        if self.tools is not None:
            self.llm.bind_tools(self.tools)
    
    def _set_system_prompt(self, prompt: str, messages: List[Any]) -> List[Any]:
        return [
            {"role": "system", "content": prompt}
        ] + messages

    async def ainvoke(self, messages: List[Any]) -> Any:
        if self.prompt is not None:
            messages = self._set_system_prompt(self.prompt, messages)
        return await self.llm.ainvoke(messages)
    
    def invoke(self, messages: List[Any]) -> Any:
        if self.prompt is not None:
            messages = self._set_system_prompt(self.prompt, messages)
        return self.llm.invoke(messages)
    
    async def astream(self, messages: List[Any]) -> AsyncGenerator[Any, None]:
        if self.prompt is not None:
            messages = self._set_system_prompt(self.prompt, messages)
        return await self.llm.astream(messages)
    
    def stream(self, messages: List[Any]) -> Generator[Any, None, None]:
        if self.prompt is not None:
            messages = self._set_system_prompt(self.prompt, messages)
        return self.llm.stream(messages)
