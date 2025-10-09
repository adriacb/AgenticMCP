from mcpagent.core.domain.interfaces import ToolRegistryInterface
from inspect import signature
from pydantic import BaseModel, create_model, Field
from .tool import Tool
from typing import Dict, Optional


def infer_args_schema(func) -> type[BaseModel]:
    """
    Create a Pydantic model automatically from a Python function signature.
    """
    sig = signature(func)
    fields = {}
    for name, param in sig.parameters.items():
        annotation = param.annotation if param.annotation != param.empty else str
        default = param.default if param.default != param.empty else ...
        fields[name] = (annotation, Field(default=default))
    model = create_model(f"{func.__name__.title()}Args", __base__=BaseModel, **fields)
    return model


class InMemoryToolRegistry(ToolRegistryInterface):
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        # keep a name->Tool map for execution later
        self._by_name: Dict[str, Tool] = {}

    def add(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool with name {tool.name} already exists.")
        self._tools[tool.name] = tool
        self._by_name[tool.name] = tool  # ensure .get() works during execution

    def get(self, name: str) -> Optional[Tool]:
        return self._by_name.get(name)

    def remove(self, name: str) -> None:
        if name in self._tools:
            del self._tools[name]
            self._by_name.pop(name, None)
        else:
            raise ValueError(f"Tool with name {name} does not exist.")

    def list(self) -> list:
        """
        Return tools in **OpenAI tool dict** format, with:
          - function.strict = True
          - function.parameters.additionalProperties = False
        """
        openai_tools: list[dict] = []

        for t in self._tools.values():
            # --- Build JSON Schema for parameters from Pydantic v2 model ---
            if t.args_schema is not None and hasattr(
                t.args_schema, "model_json_schema"
            ):
                params = t.args_schema.model_json_schema()
                # Normalize root to object schema
                if params.get("type") != "object":
                    params["type"] = "object"
                params.setdefault("properties", {})

                # Compute `required` from model fields if missing
                if "required" not in params:
                    required = [
                        name
                        for name, field in t.args_schema.model_fields.items()
                        if field.is_required()
                    ]
                    if required:
                        params["required"] = required
            else:
                # Fallback: empty object
                params = {"type": "object", "properties": {}}

            # 👇 REQUIRED by OpenAI’s strict tool parser
            params["additionalProperties"] = False

            tool_dict = {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": params,
                    # 👇 REQUIRED by OpenAI’s parse() path
                    "strict": True,
                },
            }

            print("DEBUG OpenAI tool schema:", tool_dict)  # keep your debug
            openai_tools.append(tool_dict)

        return openai_tools
