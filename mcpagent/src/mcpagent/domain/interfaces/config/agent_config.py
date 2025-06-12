from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AgentConfig:
    """Configuration for an agent in the application layer.
    
    This configuration defines how an agent should be set up and behave,
    including its parameters.
    """
    # Core configuration
    name: str
    description: str
        
    # parameters
    learning_rate: float = 0.1
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: int = 0
    stop: Optional[List[str]] = None
    stream: bool = False
    max_retries: int = 3
    n: Optional[int] = 1
    logprobs: Optional[bool] = None


