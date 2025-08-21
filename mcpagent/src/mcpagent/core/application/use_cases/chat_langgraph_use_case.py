from mcpagent.core.application.dto import ChatAgentInput, ChatAgentOutput
from mcpagent.infrastructure.logger import LoggerInitializer
from langgraph.graph import StateGraph

logger = LoggerInitializer.get_default_logger()

class ChatLangGraphUseCase:
    """Use case for handling chat interactions with a language model."""
    
    def __init__(self, graph: StateGraph):
        self.graph = graph # It should be .compile() complied graph
    
    async def __call__(self, input: ChatAgentInput) -> ChatAgentOutput:
        """Run the chat interaction with the language model."""
        logger.info(f"Processing input: {input}")
        
        # Validate input (should be done in the input model)
        if not input.messages:
            raise ValueError("Messages cannot be empty")
        
        # Process the input with the graph
        response = await self.graph.process(input.messages)
        
        # Log the response
        logger.info(f"Generated response: {response}")
        
        # Return the output
        return ChatAgentOutput(response=response, metadata={"source": "ChatLangGraph"})