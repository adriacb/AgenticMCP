from typing import Union

from langchain.chat_models import init_chat_model

from mcpagent.core.domain.interfaces import LLMInterface, ToolRegistryInterface, BaseMessage
from mcpagent.core.domain.value_objects import LLMConfig

class ChatLLM(LLMInterface):
    """
    Represents a Language Model (LLM) that can generate responses based on input messages.
    """
    def __init__(self, llm_config: LLMConfig, tool_registry: Union[ToolRegistryInterface,None]=None):
        """
        Initialize the LLM with the given configuration.
        
        :param llm_config: Configuration dictionary for the LLM.
        """
        self.llm_config: LLMConfig = llm_config
        self.tool_registry: Union[ToolRegistryInterface, None] = tool_registry
        self.llm = self._initialize_llm()

        # Additional initialization logic can be added here
    
    def _initialize_llm(self):
        """
        Private method to initialize the LLM based on the configuration.
        """
        if self.tool_registry is not None:
            # Initialize the LLM with the tool registry if provided
            return init_chat_model(**self.llm_config.model_dump()).bind_tools(self.tool_registry.list())
        else:
            # Initialize the LLM without a tool registry
            return init_chat_model(**self.llm_config.model_dump())
    
    def _handle_tool_calls(self, result):
        """
        Handle tool calls if any are present in the result.
        
        :param result: The result from the LLM invocation.
        """
        if hasattr(result, 'tool_calls'):
            for tool_call in result.tool_calls:
                tool = self.tool_registry.get(tool_call['name'])
                if tool:
                    # Execute the tool with the provided arguments
                    tool_response = tool.execute(**tool_call['args'])
                    # Append the tool response to the result
                    result.content += f"\nTool {tool.name} response: {tool_response}"

        return result          

    def generate(self, prompt: str) -> str:
        """
        Generate a response based on the provided messages.
        """
        return self.llm.generate(prompt)

    async def agenerate(self, prompt: str) -> str:
        """
        Asynchronously generate a response based on the provided messages.
        """
        return await self.llm.agenerate(prompt)
    
    def invoke(self, messages: list) -> str:
        """
        Invoke the LLM with the provided messages and return the response.
        
        :param messages: List of messages to send to the LLM.
        :return: The generated response as a string.
        """
        result = self.llm.invoke(messages)
        result = self._handle_tool_calls(result)
        return result
    
    async def ainvoke(self, messages: list) -> str:
        """
        Asynchronously invoke the LLM with the provided messages and return the response.
        
        :param messages: List of messages to send to the LLM.
        :return: The generated response as a string.
        """
        result = await self.llm.ainvoke(messages)
        result = self._handle_tool_calls(result)
        return result