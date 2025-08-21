# Agent configuration (AgentConfig)

This document describes the domain value object used to configure Agents in this project.

Files
- [`mcpagent/src/mcpagent/core/domain/value_objects/agent_config.py`](mcpagent/src/mcpagent/core/domain/value_objects/agent_config.py) — `AgentConfig`
- [`mcpagent/src/mcpagent/core/domain/value_objects/llm_config.py`](mcpagent/src/mcpagent/core/domain/value_objects/llm_config.py) — `LLMConfig`
- [`mcpagent/src/mcpagent/core/domain/value_objects/agent_card.py`](mcpagent/src/mcpagent/core/domain/value_objects/agent_card.py) — `AgentCard`
- [`mcpagent/src/mcpagent/core/domain/entities/agent.py`](mcpagent/src/mcpagent/core/domain/entities/agent.py) — `Agent` uses `AgentConfig`
- [`mcpagent/src/mcpagent/core/domain/entities/llm.py`](mcpagent/src/mcpagent/core/domain/entities/llm.py) — `ChatLLM` uses `LLMConfig`

Purpose
- `AgentConfig` groups all configuration required to create a domain `Agent` (LLM config, descriptive card, system prompt, ...).
- Keep configuration as a value object (immutable-ish data carrier) in `core/domain/value_objects/`.

AgentConfig schema (summary)
- llm_config: `LLMConfig` — configuration for the underlying LLM (model, temperature, tokens, etc.)
- agent_card: `AgentCard` — human-facing metadata for the agent (name, description, skills, etc.). Default is `AgentCard()` so fields have sensible defaults.
- system_prompt: str or Any — default system-level prompt for the agent.

LLMConfig (summary)
- model: str
- temperature: float
- max_tokens, top_p, frequency_penalty, presence_penalty, stop_sequences, ...
- Located at `core/domain/value_objects/llm_config.py`.

AgentCard (summary)
- name: str (default "Default Assistant")
- description: str (default "A default assistant configuration.")
- version: str (default "1.0.0")
- skills: list[dict] (default empty list)

Example usage (Python)
- Construct value objects and create an Agent:

```python
# filepath: example_usage.py
from mcpagent.core.domain.value_objects.llm_config import LLMConfig
from mcpagent.core.domain.value_objects.agent_card import AgentCard
from mcpagent.core.domain.value_objects.agent_config import AgentConfig
from mcpagent.core.domain.entities.agent import Agent
from mcpagent.core.domain.interfaces.tool_registry_interface import ToolRegistryInterface

# create LLM config
llm_cfg = LLMConfig(model="gpt-4", temperature=0.5)

# create agent card (metadata)
card = AgentCard(name="Research Assistant", description="Helps with research tasks")

# create agent config
agent_cfg = AgentConfig(llm_config=llm_cfg, agent_card=card, system_prompt="You assist with research.")

# optionally provide a tool registry (implement ToolRegistryInterface)
tool_registry: ToolRegistryInterface | None = None

# create domain agent
agent = Agent(config=agent_cfg, tool_registry=tool_registry)
```

Notes and best practices
- Location: keep value objects in `core/domain/value_objects/` and entities in `core/domain/entities/`.
- Serialization: when passing `LLMConfig` to third‑party initializers use Pydantic v2 API `model_dump()` (e.g. `init_chat_model(**llm_config.model_dump())`).
- Tests: avoid initializing real external LLM clients in unit tests.
  - Monkeypatch `ChatLLM._initialize_llm` to return a dummy model, or monkeypatch the module helper used to create the model (see `tests/unit/core/domain/test_llm.py`).
  - Example test monkeypatch:
    - `monkeypatch.setattr("mcpagent.core.domain.entities.llm.ChatLLM._initialize_llm", lambda self: DummyModel())`
- Tools: `Agent` accepts an optional `tool_registry`. The `ChatLLM` will bind tools when a registry is provided — ensure your registry implements `ToolRegistryInterface` (`core/domain/interfaces/tool_registry_interface.py`).

Common pitfalls
- Pydantic model fields must be annotated (Pydantic v2). Do not assign attributes without a type annotation in models (e.g. `skills: list[dict] = []` is OK but avoid plain `skills = []`).
- Keep default mutable fields explicit (good practice: `skills: list[dict] = []` is used here; if you prefer avoid hidden shared mutables use `field(default_factory=list)` pattern).

References
- `AgentConfig` implementation: [mcpagent/src/mcpagent/core/domain/value_objects/agent_config.py](mcpagent/src/mcpagent/core/domain/value_objects/agent_config.py)
- `LLMConfig` implementation: [mcpagent/src/mcpagent/core/domain/value_objects/llm_config.py](mcpagent/src/mcpagent/core/domain/value_objects/llm_config.py)
- `Agent` entity: [mcpagent/src/mcpagent/core/domain/entities/agent.py](mcpagent/src/mcpagent/core/domain/entities/agent.py)
- `ChatLLM` entity: [mcpagent/src/mcpagent/core/domain/entities/llm.py](mcpagent/src/mcpagent/core/domain/entities/llm.py)