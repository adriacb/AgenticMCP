from core.domain.entities import Agent
from core.domain.entities.prompt_repository import InMemoryPromptRepository
from core.domain.value_objects import AgentConfig, AgentCard, LLMConfig
from core.domain.interfaces import ToolRegistryInterface


class CreateAgent:
    """Use case to create a generic Agent."""

    def __call__(
        self,
        llm_config: LLMConfig,
        agent_card: AgentCard,
        prompt_repository: InMemoryPromptRepository,
        tool_registry: ToolRegistryInterface | None = None,
    ) -> Agent:
        """
        Create and return an Agent instance.

        Args:
            llm_config: Configuration for the LLM backend.
            agent_card: Metadata and identifiers for the agent.
            prompt_repository: In-memory repository holding system/user prompts.
            tool_registry: Optional registry of tools the agent can use.

        Returns:
            Agent: A fully constructed agent ready to run.
        """

        agent_cfg = AgentConfig(
            llm_config=llm_config,
            agent_card=agent_card,
            system_prompt=prompt_repository.get_prompt(agent_card.system_prompt_key),
        )

        return Agent(agent_cfg, tool_registry)
