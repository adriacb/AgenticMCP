from mcpagent.core.domain.entities.agent import Agent
from mcpagent.core.domain.value_objects import AgentConfig
from mcpagent.core.domain.interfaces import ToolRegistryInterface
from mcpagent.core.application.dto import ChatAgentInput, ChatAgentOutput

from mcpagent.infrastructure.logger import LoggerInitializer

logger = LoggerInitializer.get_default_logger()

class ChatAgentUseCase:
    def __init__(self, config: AgentConfig, tool_registry: ToolRegistryInterface):
        self.agent = Agent(config=config, tool_registry=tool_registry)
    
    async def __call__(self, input: ChatAgentInput) -> ChatAgentOutput:
        logger.info(f"Processing input: {input}")
        
        # Validate input (should be done in the input model)
        if not input.query:
            raise ValueError("Query cannot be empty")
        
        # Process the input with LLM
        response = await self.agent.invoke(
            query=input.query,
            tools=input.tools,
            context=input.context
        )
        
        # Log the response
        logger.info(f"Generated response: {response}")
        
        # Return the output
        return ChatAgentOutput(response=response, metadata={"source": "ChatAgent"})