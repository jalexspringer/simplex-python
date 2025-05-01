# SimpleX Python SDK

A modern, async-first Python client for the SimpleX Chat protocol. This project is a complete Python port of the TypeScript SDK for SimpleX Chat, providing a strongly-typed, high-level API for interacting with SimpleX servers.

## Features

- **Fully Async**: Built on Python's asyncio ecosystem with proper async context managers and generators
- **Strongly Typed**: Uses Python 3.13+ type hints, dataclasses, and PEP 695 generics for modern, type-safe code
- **WebSocket Transport**: Reliable WebSocket-based communication with the SimpleX protocol
- **Command & Response Modeling**: Comprehensive dataclass representations of all protocol commands and responses
- **Request/Response Correlation**: Automatic tracking of command correlation IDs
- **Event Streaming**: Async generators for server events and notifications
- **Error Handling**: Proper exception hierarchies and timeouts
- **Modern Python**: Uses the latest Python 3.13+ idioms and patterns

## Installation

```bash
pip install simplex-python-sdk
```

## Quick Start

```python
import asyncio
from simplexbot.client import SimplexClient
from simplexbot.command import ShowActiveUser, StartChat, Profile, APISetActiveUser

async def main():
    # Connect to a SimpleX chat server
    async with SimplexClient("ws://localhost:5225") as client:
        # Check who is the active user
        resp = await client.send_command(ShowActiveUser())
        print(f"Active user: {resp.resp.user.display_name}")
        
        # Start a chat session
        await client.send_command(StartChat(subscribe_connections=True))
        
        # Listen for events from the server
        async for event in client.events():
            print(f"Received event: {event.resp.type}")
            
            # Process different event types
            if hasattr(event.resp, "type") and event.resp.type == "newChatItems":
                print(f"New messages for {event.resp.user.display_name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Components

### SimplexClient

The primary interface for interacting with SimpleX Chat servers:

```python
from simplexbot.client import SimplexClient

# Connect using a URL
client = SimplexClient("ws://localhost:5225")

# Or use a server object
from simplexbot.transport import ChatServer
server = ChatServer(host="localhost", port="5225")
client = SimplexClient(server)

# Use as an async context manager
async with SimplexClient("ws://localhost:5225") as client:
    # Work with the client
    ...
```

### Commands

The SDK provides dataclasses for all SimpleX Chat commands:

```python
from simplexbot.command import (
    ShowActiveUser,
    CreateActiveUser,
    APISetActiveUser,
    StartChat,
    Profile,
    APISendMessage,
    MsgContent,
    ComposedMessage,
    ChatType
)

# Create a new user profile
profile = Profile(
    display_name="Alice",
    full_name="Alice Smith"
)

# Create a user with this profile
cmd = CreateActiveUser(profile=profile)

# Send a text message
msg_content = MsgContent(type="text", text="Hello, world!")
message = ComposedMessage(msg_content=msg_content)
send_cmd = APISendMessage(
    chat_type=ChatType.DIRECT,
    chat_id=123,
    messages=[message]
)
```

### Responses

Responses from the server are typed with appropriate dataclasses:

```python
from simplexbot.response import (
    CRActiveUser,
    CRChatStarted,
    CRNewChatItems
)

# Responses are returned from send_command
resp = await client.send_command(ShowActiveUser())
if resp.resp.type == "activeUser":
    active_user = resp.resp.user
    print(f"Active user: {active_user.display_name}")

# Events can be processed in a loop
async for event in client.events():
    if hasattr(event.resp, "type"):
        if event.resp.type == "chatStarted":
            print("Chat session started")
        elif event.resp.type == "newChatItems":
            print(f"New messages received in {event.resp.chat_items[0].chat_id}")
```

## Transport Layer

The SDK uses a layered approach to communication:

1. **WSTransport**: Low-level WebSocket transport using websockets library
2. **ChatTransport**: Protocol-aware transport with serialization/deserialization
3. **SimplexClient**: High-level client with command correlation and event handling

You can access the transport directly if needed:

```python
from simplexbot.transport import ChatTransport, ChatServer

server = ChatServer(host="localhost", port="5225")
transport = await ChatTransport.connect(server)

# Manually send and receive
await transport.write(request)
response = await transport.read()
```

## Async Queue

The SDK includes a robust async bounded queue implementation:

```python
from simplexbot.queue import ABQueue

# Create a bounded queue with max size
queue = ABQueue[str](100)

# Producer
await queue.enqueue("item")

# Consumer
item = await queue.dequeue()

# Async iteration
async for item in queue:
    print(item)

# Close the queue
await queue.close()
```

## Error Handling

The SDK provides various error types for proper exception handling:

```python
from simplexbot.client import SimplexClientError
from simplexbot.transport import TransportError
from simplexbot.queue import ABQueueError

try:
    await client.send_command(cmd, timeout=5.0)
except SimplexClientError as e:
    print(f"Client error: {e}")
except TransportError as e:
    print(f"Transport error: {e}")
except ABQueueError as e:
    print(f"Queue error: {e}")
```

## Chat Features

The SDK supports all SimpleX Chat features including:

### User Management

```python
# Create a new user
profile = Profile(display_name="Bob", full_name="Bob Johnson")
await client.send_command(CreateActiveUser(profile=profile))

# List all users
users_resp = await client.send_command(ListUsers())
for user in users_resp.resp.users:
    print(f"User: {user.display_name}")

# Switch active user
await client.send_command(APISetActiveUser(user_id=123))
```

### Messaging

```python
# Send a text message
msg = MsgContent(type="text", text="Hello!")
composed = ComposedMessage(msg_content=msg)
await client.send_command(APISendMessage(
    chat_type=ChatType.DIRECT,
    chat_id=456,
    messages=[composed]
))

# Update a message
await client.send_command(APIUpdateChatItem(
    chat_type=ChatType.DIRECT,
    chat_id=456,
    chat_item_id=789,
    msg_content=MsgContent(type="text", text="Updated message")
))

# Delete a message
await client.send_command(APIDeleteChatItem(
    chat_type=ChatType.DIRECT,
    chat_id=456,
    chat_item_id=789,
    delete_mode=DeleteMode.BROADCAST
))
```

### Group Management

```python
# Create a new group
group_profile = GroupProfile(
    display_name="Project Team",
    full_name="Project Alpha Team"
)
group_resp = await client.send_command(NewGroup(group_profile=group_profile))

# Add a member to the group
await client.send_command(APIAddMember(
    group_id=group_resp.resp.group_id,
    contact_id=123,
    member_role=GroupMemberRole.MEMBER
))

# Create a group invite link
link_resp = await client.send_command(APICreateGroupLink(
    group_id=group_resp.resp.group_id,
    member_role=GroupMemberRole.MEMBER
))
```

### Contact Management

```python
# Accept a contact request
await client.send_command(APIAcceptContact(contact_req_id=123))

# Reject a contact request
await client.send_command(APIRejectContact(contact_req_id=456))

# Set a contact alias
await client.send_command(APISetContactAlias(
    contact_id=123,
    local_alias="Work Alice"
))
```

### File Transfer

```python
# Receive a file
await client.send_command(ReceiveFile(
    file_id=123,
    file_path="/path/to/save/file.jpg"
))

# Cancel file transfer
await client.send_command(CancelFile(file_id=123))

# Check file status
status_resp = await client.send_command(FileStatus(file_id=123))
```

## Advanced Usage

### Custom Correlation IDs

```python
from uuid import uuid4

# Manually set correlation ID
cmd = ShowActiveUser()
cmd.corr_id = str(uuid4())
resp = await client.send_command(cmd)
```

### Custom Timeouts

```python
# Set longer timeout for this specific command
resp = await client.send_command(APIGetChats(user_id=123), timeout=30.0)

# Or set default timeout at client creation
client = SimplexClient("ws://localhost:5225", timeout=15.0)
```

### Event Filtering

```python
async for event in client.events():
    if hasattr(event.resp, "type"):
        # Filter by event type
        if event.resp.type == "newChatItems":
            # Process new messages
            pass
        elif event.resp.type == "chatItemStatusUpdated":
            # Process status updates
            pass
```

## Development

### Requirements

- Python 3.13+
- websockets library

### Testing

```bash
pytest tests/
```

## License

[MIT License](LICENSE)