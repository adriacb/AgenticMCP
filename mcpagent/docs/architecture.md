# AgenticMCP Architecture

This document outlines the architecture of the AgenticMCP project, following clean architecture principles.

## Overview

The project is organized into four main layers:

1. **Domain Layer**: Core business rules and entities
2. **Application Layer**: Use cases and their interfaces
3. **Infrastructure Layer**: External implementations and adapters
4. **Presentation Layer**: User-facing interfaces

## Layer Details

### Domain Layer

The domain layer contains the core business rules and entities. It has no dependencies on other layers.

#### Structure
```
domain/
├── entities/              # Core business objects
├── interfaces/            # Abstract definitions
├── value_objects/         # Immutable domain objects
├── repositories/          # Repository interfaces
└── __init__.py
```

#### Key Components
- **Connection Types**: Define different ways to connect to MCP servers
  - `StdioConnection`: Standard I/O based connection
  - `SSEConnection`: Server-Sent Events connection
  - `StreamableHttpConnection`: HTTP streaming connection
  - `WebsocketConnection`: WebSocket based connection
- **Session Interface**: Defines the contract for MCP sessions
  - `Session`: Base interface
  - `StreamableSession`: Interface for streaming capability
  - `SessionFactory`: Protocol for creating sessions

### Application Layer

The application layer contains use cases and their interfaces. It depends only on the domain layer.

#### Structure
```
application/
├── interfaces/
│   ├── tool_loader.py      # Interface for loading tools
│   ├── prompt_loader.py    # Interface for loading prompts
│   ├── resource_loader.py  # Interface for loading resources
│   └── session_manager.py  # Interface for managing sessions
├── use_cases/
│   ├── tools/
│   ├── prompts/
│   ├── resources/
│   └── sessions/
└── __init__.py
```

#### Key Components
- **Tool Loading**: Interface for loading tools from MCP sessions
- **Prompt Loading**: Interface for loading prompts from MCP sessions
- **Resource Loading**: Interface for loading resources from MCP sessions
- **Session Management**: Interface for managing MCP sessions

### Infrastructure Layer

The infrastructure layer contains implementations of the application layer interfaces and external dependencies.

#### Structure
```
infrastructure/
└── external/
    └── mcp/
        ├── base_session.py      # Base session implementation
        ├── client.py            # MCP client implementation
        ├── client_session.py    # Client session implementation
        ├── constants.py         # Implementation constants
        ├── session_factory.py   # Session factory implementation
        ├── sse.py              # SSE connection implementation
        ├── stdio.py            # Stdio connection implementation
        ├── streamable_http.py   # Streamable HTTP implementation
        └── websocket.py        # WebSocket connection implementation
```

#### Key Components
- **Session Implementations**:
  - `BaseSession`: Common session functionality
  - `ClientSession`: Client-side session implementation
- **Connection Implementations**:
  - `StreamableHttp`: HTTP streaming implementation
  - `SSE`: Server-Sent Events implementation
  - `Stdio`: Standard I/O implementation
  - `Websocket`: WebSocket implementation
- **Session Factory**: Creates appropriate session types based on connection configuration

#### Streamable HTTP Implementation

The Streamable HTTP implementation provides a robust way to handle streaming HTTP connections with the MCP server. Key features include:

- **Protocol-based Design**: Uses Python's Protocol class for type-safe client factory definitions
- **Lazy Loading**: Imports external dependencies (like `httpx`) only when needed
- **Configurable Timeouts**: Default timeouts with ability to override:
  - `DEFAULT_STREAMABLE_HTTP_TIMEOUT`: 30 seconds for HTTP operations
  - `DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT`: 5 minutes for SSE event reading
- **Resource Management**: Proper cleanup of resources using async context managers
- **Type Safety**: Comprehensive type hints with runtime import protection using `TYPE_CHECKING`

The implementation is designed to be testable with:
- Mockable HTTP client factory
- Configurable timeouts and headers
- Proper error handling for missing dependencies
- Support for custom session parameters

### Presentation Layer

The presentation layer provides the user-facing interface. It depends on the application layer.

#### Structure
```
presentation/
├── client/
│   ├── mcp_client.py      # High-level client API
│   └── __init__.py
└── __init__.py
```

#### Key Components
- **MultiServerMCPClient**: Main client class for users to interact with MCP servers

## Design Principles

1. **Dependency Rule**: Dependencies point inward. Outer layers depend on inner layers, not vice versa.
2. **Interface Segregation**: Each layer defines clear interfaces for its functionality.
3. **Single Responsibility**: Each component has a single, well-defined responsibility.
4. **Dependency Inversion**: High-level modules don't depend on low-level modules. Both depend on abstractions.

## Usage Example

```python
from mcpagent import MultiServerMCPClient

# Create a client with server connections
client = MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": ["/path/to/math_server.py"],
        "transport": "stdio",
    },
    "weather": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http",
    }
})

# Get tools from all servers
all_tools = await client.get_tools()

# Get tools from a specific server
math_tools = await client.get_tools(server_name="math")

# Get a prompt
prompt = await client.get_prompt("math", "calculator", arguments={"operation": "add"})

# Get resources
resources = await client.get_resources("weather", uris=["forecast.json"])

# Use a session directly
async with client.session("math") as session:
    # Do something with the session
    pass
```

## Future Improvements

1. **Infrastructure Implementation**: Complete the infrastructure layer implementations
2. **Error Handling**: Add comprehensive error handling and recovery
3. **Testing**: Add unit and integration tests for each layer
4. **Documentation**: Add more detailed documentation for each component
5. **Monitoring**: Add logging and monitoring capabilities 