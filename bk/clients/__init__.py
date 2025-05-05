"""
Domain-specific clients for the Simplex Chat protocol.

This package contains client implementations for specific domains:
- users: User management
- groups: Group management
- chats: Chat messaging
- files: File operations
- database: Database and archive management
- connections: Contact and connection management
"""

from .users import UsersClient
from .groups import GroupsClient
from .chats import ChatsClient
from .files import FilesClient
from .database import DatabaseClient
from .connections import ConnectionsClient

__all__ = [
    "UsersClient",
    "GroupsClient",
    "ChatsClient",
    "FilesClient",
    "DatabaseClient",
    "ConnectionsClient",
]
