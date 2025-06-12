from abc import ABC, abstractmethod
from typing import List, Optional, Any

from mcpagent.domain.interfaces.session import Session

class ResourceLoader(ABC):
    """Interface for loading resources from an MCP session."""

    @abstractmethod
    async def load_resources(
        self,
        session: Session,
        uris: Optional[List[str]] = None,
    ) -> List[Any]:
        """Load resources from an MCP session.

        Args:
            session: The session to load resources from
            uris: Optional list of URIs to load resources from.
                If not provided, all resources will be loaded.

        Returns:
            A list of loaded resources
        """
        pass 