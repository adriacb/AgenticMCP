from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class ToolConfig:
    """Value object for tool configuration."""
    
    name: str
    description: str
    parameters: Dict[str, Any]
    enabled: bool = True
    timeout: Optional[int] = None
    max_retries: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the config to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "enabled": self.enabled,
            "timeout": self.timeout,
            "max_retries": self.max_retries
        } 