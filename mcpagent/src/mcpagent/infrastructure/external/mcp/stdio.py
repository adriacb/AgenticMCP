from typing import Any, AsyncIterator, Optional, Literal
from contextlib import asynccontextmanager
import os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_ENCODING = "utf-8"
DEFAULT_ENCODING_ERROR_HANDLER: Literal["strict", "ignore", "replace"] = "strict"

@asynccontextmanager
async def create_stdio_session(
    command: str,
    args: list[str],
    env: Optional[dict[str, str]] = None,
    cwd: Optional[str | Path] = None,
    encoding: str = DEFAULT_ENCODING,
    encoding_error_handler: Literal["strict", "ignore", "replace"] = DEFAULT_ENCODING_ERROR_HANDLER,
    session_kwargs: Optional[dict[str, Any]] = None,
) -> AsyncIterator[ClientSession]:
    """Create a new session to an MCP server using stdio

    Args:
        command: Command to execute
        args: Arguments for the command
        env: Environment variables for the command
        cwd: Working directory for the command
        encoding: Character encoding
        encoding_error_handler: How to handle encoding errors
        session_kwargs: Additional keyword arguments to pass to the ClientSession
    """
    # NOTE: execution commands (e.g., `uvx` / `npx`) require PATH envvar to be set.
    # To address this, we automatically inject existing PATH envvar into the `env` value,
    # if it's not already set.
    env = env or {}
    if "PATH" not in env:
        env["PATH"] = os.environ.get("PATH", "")

    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=env,
        cwd=cwd,
        encoding=encoding,
        encoding_error_handler=encoding_error_handler,
    )

    # Create and store the connection
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, **(session_kwargs or {})) as session:
            yield session 