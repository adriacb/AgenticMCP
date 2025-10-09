from mcpagent.core.domain.interfaces import PromptRegistryInterface
from mcpagent.core.domain.entities import InMemoryPromptRepository, ChatLLM, AIMessage
from mcpagent.core.domain.value_objects import AgentConfig, AgentCard, LLMConfig
from mcpagent.infrastructure.langgraph.react_agent.states import State
from mcpagent.infrastructure.logger import LoggerInitializer

class CallModelFunctionNode:
    def __init__(self, 
                 agent_config: AgentConfig|None = None, 
                 prompt_repository: PromptRegistryInterface|None = None,
                 tools: list = []
                 ):
        self.agent_config = agent_config
        self.prompt_repository = prompt_repository or InMemoryPromptRepository() # default prompt repository
        self.llm = None
        self.logger = LoggerInitializer.get_default_logger()
        self.context_config: dict = {}
        self.tools = tools

    def configure(self):
        if not self.agent_config:
            self.logger.info("No agent config provided, using default ReACT config.")
            # Default ReACT config
            llm_cfg = LLMConfig(model="gpt-4o-mini", temperature=0.0)
            card = AgentCard(
                name="A ReACT agent.", description="Has access to tools and uses them when needed."
            )
            self.agent_config = AgentConfig(
                llm_config=llm_cfg,
                agent_card=card,
                system_prompt="""You are a helpful AI agent that uses tools to assist with user queries.
                You might want to use more than tool if needed.
                Ask yourself: Do I still need a tool?
                If yes, then keep using tools.
                """,
            )
        self.llm = ChatLLM(llm_config=self.agent_config.llm_config, tools=self.tools)
        self.context_config['max_search_results'] = 10
        return self.llm
    
    async def __call__(self, state: State):
        if not self.llm:
            self.configure()
        self.logger.info("Invoking LLM with messages: %s", state.messages)
        system_message = self.context_config.get("system_prompt", "")

        response = await self.llm.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        )

        if state.is_last_step and response.tool_calls:
            return {
                "messages": [
                    AIMessage(
                        id=response.id,
                        content="Sorry, I could not find an answer to your question in the specified number of steps.",
                    )
                ]
            }

        return {"messages": [response]}
        