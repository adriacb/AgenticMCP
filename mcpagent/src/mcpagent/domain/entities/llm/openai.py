import os
import json
from typing import Any, List, AsyncGenerator, Dict, Union, Callable
from openai import AsyncOpenAI, AsyncClient, OpenAI

from mcpagent.application.services.config import OpenAILLMConfig
from mcpagent.application.services.logger import LoggerInitializer
from mcpagent.domain.entities.tools import Tool
from mcpagent.domain.interfaces.llm import LLMInterface

logger = LoggerInitializer.get_default_logger()

class OpenAILLMClient(LLMInterface):
    """OpenAI client implementation supporting both synchronous and asynchronous operations."""
    
    def __init__(self, config: OpenAILLMConfig):
        """Initialize OpenAI LLM client.
        
        Args:
            config (OpenAIConfig): OpenAI configuration
        """
        try:
            self._config = config
            self._client = AsyncClient(api_key=config.api_key)
            self._tools: Dict[str, Tool] = {}
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            raise e

    @property
    def sync_client(self) -> OpenAI:
        """Lazy initialization of the synchronous OpenAI client."""
        if not hasattr(self, '_sync_client'):
            try:
                self._sync_client = OpenAI(api_key=self._config.api_key)
            except Exception as e:
                logger.error(f"Error initializing sync OpenAI client: {e}")
                raise e
        return self._sync_client


    @property
    def async_client(self) -> AsyncOpenAI:
        """Lazy initialization of the asynchronous OpenAI client."""
        return self._client

    def bind_tools(self, tools: List[Union[Tool, Callable]]) -> 'OpenAILLMClient':
        """Bind a list of tools to the LLM client."""
        for tool in tools:
            if callable(tool):
                tool = Tool(name=tool.__name__, function=tool, description=tool.__doc__, parameters={})
            self._tools[tool.name] = tool
        return self

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get the list of tools in OpenAI format."""
        return [tool.to_dict() for tool in self._tools.values()]

    async def _handle_tool_calls(self, response: Any, messages: List[Dict[str, Any]]) -> str:
        """Handle tool calls in the response and execute them."""
        if not hasattr(response, 'choices') or not response.choices:
            return ""
            
        message = response.choices[0].message
        if not hasattr(message, 'tool_calls') or not message.tool_calls:
            return message.content

        # Add the assistant's message with tool calls to the conversation
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls
        })

        # Execute each tool call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            result = await self._mcp_client.call_mcp_tool(tool_name, tool_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": str(result)
            })

        # Get final response from model
        response = await self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content

    def generate(self, 
                 prompt: str, 
                 instructions: str = "",
                 tools: List[Dict[str, str]] = None
                 ) -> str:
        """Generate a response for a prompt using the responses API."""
        try:
            response = self.sync_client.responses.create(
                **self._config.model_dump(),
                input=prompt,
                instructions=instructions,
                stream=False,
                tools=tools,
            )
            return response.choices[0].text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e

    async def agenerate(self, 
                        prompt: str, 
                        instructions: str = "",
                        tools: List[Dict[str, str]] = None
                        ) -> AsyncGenerator[str, None]:
        """Asynchronously generate a response for a prompt using the responses API."""
        try:
            response = await self._client.responses.create(
                model=self._config.model,
                input=prompt,
                instructions=instructions,
                stream=True,
                tools=tools,
            )
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e

    def invoke(self, 
               prompt: Union[str, List[Dict[str, str]]], 
               tools: List[Dict[str, str]] = None,
               stream: bool = False
               ) -> Union[str, AsyncGenerator[str, None]]:
        """Invoke the model with a prompt or message list."""
        try:
            messages = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
            response = self.sync_client.chat.completions.create(
                model=self._config.model,
                messages=messages,
                tools=tools,
                stream=stream,
            )
            if stream:
                return response
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error invoking model: {e}")
            raise e

    async def _ainvoke_stream(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> AsyncGenerator[str, None]:
        """Handle streaming responses with tool calls."""
        try:
            # Make the initial call
            response = await self._client.chat.completions.create(
                model=self._config.model,
                messages=messages,
                tools=tools,
                stream=True
            )

            current_message = ""
            current_tool_call = None
            
            async for chunk in response:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    current_message += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content
                
                if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                    tool_call = chunk.choices[0].delta.tool_calls[0]
                    if tool_call.id:
                        current_tool_call = tool_call
                    elif current_tool_call:
                        if tool_call.function.name:
                            current_tool_call.function.name = tool_call.function.name
                        if tool_call.function.arguments:
                            current_tool_call.function.arguments = tool_call.function.arguments
            
            # If we have a complete tool call, handle it
            if current_tool_call and current_tool_call.function.name:
                # Add the complete message with tool call
                messages.append({
                    "role": "assistant",
                    "content": current_message,
                    "tool_calls": [current_tool_call]
                })
                
                # Execute the tool call
                if current_tool_call.function.name not in self._tools:
                    logger.error(f"Tool {current_tool_call.function.name} not registered")
                else:
                    # Parse the arguments
                    try:
                        args = json.loads(current_tool_call.function.arguments)
                    except json.JSONDecodeError:
                        args = {}

                    # Execute the tool
                    try:
                        result = self._tools[current_tool_call.function.name].function(**args)
                    except Exception as e:
                        logger.error(f"Error executing tool {current_tool_call.function.name}: {e}")
                        result = f"Error: {str(e)}"

                    # Add the tool response to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": current_tool_call.id,
                        "content": str(result)
                    })

                    # Get the final response
                    final_response = await self._client.chat.completions.create(
                        model=self._config.model,
                        messages=messages,
                        stream=True
                    )
                    
                    async for chunk in final_response:
                        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Error in stream generator: {e}")
            raise e

    async def ainvoke(self,
                      messages: List[Dict[str, Any]],
                      tools: List[Dict[str, Any]] = None,
                      ) -> Union[str, AsyncGenerator[str, None]]:
        response = await self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            tools=tools,
            stream=False
        )

        if hasattr(response, 'choices') and response.choices:
            return await self._handle_tool_calls(response, messages)
        return response.choices[0].message.content

    async def astream(self, **kwargs) -> AsyncGenerator[str, None]:
        """Streaming async call. Yields chunks of the response."""
        messages = kwargs.get('messages', [])
        tools = kwargs.get('tools', self.get_tools())

        response = await self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            tools=tools,
            stream=True
        )

        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
