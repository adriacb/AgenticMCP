from fastmcp.client.logging import LogMessage


async def log_handler(message: LogMessage):
    print(f"Server log: {message.data}")


async def progress_handler(progress: float, total: float | None, message: str | None):
    print(f"Progress: {progress}/{total} - {message}")


async def sampling_handler(messages, params, context):
    # Integrate with your LLM service here
    return "Generated response"
