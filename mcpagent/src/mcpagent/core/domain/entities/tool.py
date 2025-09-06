from mcpagent.core.domain.interfaces import ToolInterface
from mcpagent.core.domain.value_objects import ToolCard

from typing import Callable, Optional, List, Type
from pydantic import BaseModel, Field, create_model
from inspect import signature


class Tool(ToolInterface):
    """
    Represents a tool that can be used by an agent.
    """

    def __init__(self, tool_card: ToolCard):
        self.name = tool_card.name
        self.description = tool_card.description
        self.tags = tool_card.tags
        self.examples = tool_card.examples
        self.parameters = tool_card.parameters
        self.function = tool_card.function
        self.args_schema = tool_card.args_schema

    def execute(self, *args, **kwargs):
        """Execute the tool with validated arguments if schema exists."""
        if self.args_schema:
            validated_args = self.args_schema(**kwargs)
            return self.function(**validated_args.dict())

        # If parameters were provided as a dict with 'args' and 'kwargs', support that
        params = getattr(self, "parameters", None) or {}
        if isinstance(params, dict) and "args" in params and "kwargs" in params:
            return self.function(*params.get("args", []), **params.get("kwargs", {}))

        return self.function(*args, **kwargs)

    def to_openai_tool(self) -> dict:
        """
        Convert this Tool into an OpenAI-compatible function schema.
        """
        schema = (
            self.args_schema.model_json_schema()
            if self.args_schema
            else {"type": "object", "properties": {}}
        )

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": schema,
                "strict": True,   # 👈 force strict mode here
            },
        }

    def __repr__(self):
        return (
            f"Tool(name={self.name}, description={self.description}, "
            f"tags={self.tags}, examples={self.examples})"
        )

    # ----------------------
    # Factory constructor
    # ----------------------
    @classmethod
    def from_function(
        cls,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        args_schema: Optional[Type[BaseModel]] = None,
        tags: Optional[List[str]] = None,
        examples: Optional[List[str]] = None,
    ):
        # Infer schema if not provided
        if args_schema is None:
            sig = signature(func)
            fields = {}
            for param_name, param in sig.parameters.items():
                ann = param.annotation if param.annotation != param.empty else str
                default = param.default if param.default != param.empty else ...
                fields[param_name] = (ann, Field(default=default))
            args_schema = create_model(
                f"{func.__name__.title()}Args",
                __base__=BaseModel,
                **fields,
            )

        tool_card = ToolCard(
            name=name or func.__name__,
            description=description or (func.__doc__ or ""),
            tags=tags or [],        # 👈 enforce list
            examples=examples or [],# 👈 enforce list
            parameters=args_schema.model_json_schema(),
            function=func,
            args_schema=args_schema,
            strict=True,   # 👈 force strict mode
        )
        return cls(tool_card)