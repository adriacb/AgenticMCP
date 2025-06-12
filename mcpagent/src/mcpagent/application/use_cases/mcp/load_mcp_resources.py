from typing import List, Optional, Any

from mcpagent.domain.interfaces.session import Session
from mcpagent.domain.interfaces.resource_loader import ResourceLoader

class LoadMCPResourcesUseCase:
    """Use case for loading resources from an MCP session."""
    
    def __init__(self, resource_loader: ResourceLoader):
        """Initialize the use case.
        
        Args:
            resource_loader: The resource loader to use
        """
        self._resource_loader = resource_loader
    
    async def execute(
        self,
        session: Session,
        uris: Optional[List[str]] = None,
    ) -> List[Any]:
        """Load resources from an MCP session.

        Args:
            session: Session to load resources from
            uris: Optional list of URIs to load resources from

        Returns:
            A list of loaded resources

        Raises:
            ValueError: If session is inactive
        """
        if not await session.is_active():
            raise ValueError("Session is not active")
            
        return await self._resource_loader.load_resources(session=session, uris=uris) 