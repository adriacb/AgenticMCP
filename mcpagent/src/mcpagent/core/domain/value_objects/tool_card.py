from typing import Callable, Any, Dict, List
from pydantic import BaseModel, Field

class ToolCard(BaseModel):
    """Metadata for a Tool used by agents."""
    name: str
    description: str = ""
    tags: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    function: Callable[..., Any]
    args_schema: Any = None  # Schema for the arguments, can be a Pydantic model or similar
    strict: bool = True
    # allow callables / other arbitrary runtime types if needed
    model_config = {"arbitrary_types_allowed": True}

    def __str__(self):
        return f"ToolCard(name={self.name}, description={self.description}, parameters={self.parameters}), tags={self.tags}, examples={self.examples})"