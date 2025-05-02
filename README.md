# SimplexPython

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)

A high-level, fully Pythonic client for the Simplex chat protocol with a fluent API design.

## 🌟 Features

- **Domain-specific clients**: Specialized clients for users, groups, chats, files, database operations, and connections
- **Strongly-typed methods**: Comprehensive type hints for better developer experience
- **Async context manager support**: Clean resource management with `async with`
- **Correlation ID tracking**: Reliable request/response matching
- **Clean separation of concerns**: Modular architecture for maintainability
- **Comprehensive error handling**: Specific error types for different failure scenarios

## 🚀 Implementation Details

This library implements the SimpleX Chat WebSocket protocol as defined in the official SimpleX Chat repository. The command structure and serialization formats are based on the Haskell implementation in [Simplex.Chat.Controller](https://github.com/simplex-chat/simplex-chat/blob/stable/src/Simplex/Chat/Controller.hs), which defines the canonical command types and their string representations.

Each command in our Python implementation requires a `type` field that maps directly to the corresponding `ChatCommand` data type in the Haskell codebase. This ensures compatibility with the SimpleX Chat server.

## 📦 Installation

```bash
pip install simplex-python
```

Requires Python 3.13 or higher due to the use of PEP 695 generics.

## 🚀 Quick Start

```python
import asyncio
from simplex_python import SimplexClient
from simplex_python.transport import ChatServer

async def main():
    # Connect to a Simplex chat server
    server = ChatServer(host="localhost", port="8080")
    async with SimplexClient(server) as client:
        # User operations
        user = await client.users.get_active()
        
        # Group operations
        group = await client.groups.create("Project Team")
        
        # Chat operations
        await client.chats.send_message(group.id, "Hello, world!")
        
        # Listen for events
        async for event in client.events():
            print(f"Received event: {event.type}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📖 Usage Examples

### Working with Users

```python
# Create a new user profile
user = await client.users.create("Display Name", "Full Name")

# Get or create a contact address
address = await client.users.get_address()
if not address:
    await client.users.create_address()
    address = await client.users.get_address()

# Enable automatic acceptance of contact requests
await client.users.enable_auto_accept(accept_incognito=True)
```

### Group Management

```python
# Create a new group
group = await client.groups.create("My Group")

# Add members to the group
await client.groups.add_member(group.id, contact_id, role="admin")

# Update group profile
await client.groups.update(group.id, "New Group Name")
```

### Messaging

```python
# Send a text message
await client.chats.send_message(chat_id, "Hello, world!")

# Get chat history
chat = await client.chats.get("direct", chat_id, count=50)

# Mark messages as read
await client.chats.mark_as_read("direct", chat_id)
```

## 🏗️ Architecture

SimplexPython follows a modular architecture with the following components:

- **Client**: The main entry point to the API, exposing domain-specific clients
- **Transport**: Handles the WebSocket communication with the server
- **Commands**: Defines all command structures sent to the server, with each command requiring a `type` attribute that corresponds to its Haskell counterpart
- **Response**: Parses and structures server responses
- **Queue**: Manages asynchronous event queues
- **Clients**: Domain-specific clients for different functional areas
- **Errors**: Specialized error types for different failure scenarios

## 🧩 Project Structure

```
simplex_python/
├── __init__.py
├── client.py           # Main client interface
├── transport.py        # Transport abstraction
├── queue.py            # Async bounded queue implementation
├── response.py         # Response type definitions
├── cmds/               # Command type definitions
│   ├── __init__.py
│   ├── base.py         # Base command class with required 'type' attribute
│   ├── command_formatting.py  # Converts commands to protocol strings
│   ├── chats.py
│   ├── commands.py     # Re-exports from all command modules
│   ├── users.py
│   └── ...
├── clients/            # Domain-specific client implementations
│   ├── __init__.py
│   ├── users.py
│   ├── chats.py
│   ├── groups.py
│   └── ...
└── errors.py           # Error types
```

## 🧪 Running Tests

```bash
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

When implementing new commands, ensure that:
1. Each command class has a required `type` attribute
2. The `type` value matches the corresponding command in SimpleX Chat's Controller.hs
3. Command serialization follows the format defined in the Haskell codebase

## 🙏 Acknowledgements

- The Simplex Chat team for creating the protocol and [open-sourcing](https://github.com/simplex-chat/simplex-chat) the reference implementation