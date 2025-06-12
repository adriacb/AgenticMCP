from abc import ABC, abstractmethod
from typing import Optional

from mcpagent.domain.interfaces.session import Session

class PromptLoader(ABC):
    """Interface for loading prompts from an MCP session."""

    @abstractmethod
    async def load_prompt(self, session: Session) -> str:
        """Load a prompt from an MCP session.

        Args:
            session: The session to load the prompt from

        Returns:
            The loaded prompt text
        """
        pass 