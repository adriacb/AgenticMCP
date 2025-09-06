from inspect import signature
from typing import Callable, Optional, Any
from pydantic import BaseModel, create_model
from mcpagent.core.domain.interfaces import ToolRegistryInterface
from mcpagent.core.domain.entities import Tool


def infer_args_schema(func) -> type[BaseModel]:
    """
    Create a Pydantic model automatically from a Python function signature.
    """
    sig = signature(func)
    fields = {}
    for name, param in sig.parameters.items():
        annotation = param.annotation if param.annotation != param.empty else Any
        default = param.default if param.default != param.empty else ...
        fields[name] = (annotation, default)
    model = create_model(f"{func.__name__.title()}Args", **fields)
    return model


def tool(func: Callable = None, *, registry: Optional["ToolRegistryInterface"] = None):
    """
    Decorator to wrap a function into a Tool and optionally register it.
    """
    if func is None:
        return lambda f: tool(f, registry=registry)

    # Build our custom Tool
    wrapped_tool = Tool.from_function(func)

    if registry is not None:
        registry.add(wrapped_tool)

    return wrapped_tool
