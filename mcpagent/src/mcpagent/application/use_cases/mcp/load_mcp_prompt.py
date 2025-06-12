from typing import Optional, Any

from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.prompt_loader import PromptLoader

class LoadMCPPromptUseCase:
    """Use case for loading prompts from an MCP session."""
    
    def __init__(self, prompt_loader: PromptLoader):
        """Initialize the use case.
        
        Args:
            prompt_loader: The prompt loader to use
        """
        self._prompt_loader = prompt_loader
    
    async def execute(
        self,
        session: Session,
        name: str,
        *,
        arguments: Optional[dict[str, Any]] = None,
    ) -> str:
        """Load a prompt from an MCP session.

        Args:
            session: Session to load prompt from
            name: Name of the prompt to load
            arguments: Optional arguments for the prompt

        Returns:
            The loaded prompt text

        Raises:
            ValueError: If session is inactive
        """
        if not await session.is_active():
            raise ValueError("Session is not active")
            
        return await self._prompt_loader.load_prompt(session=session, name=name, arguments=arguments) 