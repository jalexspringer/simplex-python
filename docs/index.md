# SimplexPython SDK

A type-safe, async-first Python SDK for interacting with the SimpleX Chat server.

## Overview

SimplexPython provides a comprehensive and strongly-typed interface to the SimpleX Chat protocol. 
The SDK is designed with modern Python features and follows best practices for Python 3.13.

## Key Features

- **Async-first design** for efficient network operations
- **Strong typing** with PEP 695 generics and comprehensive type hints
- **Fluent API** with domain-specific clients
- **Clean separation of concerns** between transport, commands, and responses
- **Extensive error handling** with detailed error messages

## Installation

```bash
pip install simplex-python
```

## Quick Start

```python
import asyncio
from simplex_python.client import SimplexClient

async def main():
    async with SimplexClient("ws://localhost:5225") as client:
        # Get the active user
        active_user = await client.users.get_active()
        print(f"Active user: {active_user.display_name}")
        
        # List all users
        users = await client.users.list_users()
        print(f"Found {len(users)} users")
        
        # Create a new user with auto-created profile address
        new_user = await client.users.create_active_user(
            display_name="Alice", 
            full_name="Alice Smith"
        )
        print(f"Created user: {new_user.display_name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Documentation

The SDK is organized into domain-specific clients:

- [Client API](api/client.md) - Main client interface
- [Users API](api/users.md) - User management operations
