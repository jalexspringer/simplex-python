"""
Chat management command classes for the Simplex messaging system.

This module defines the commands for managing chats, including:
- Starting and stopping chats
- Retrieving chat information
- Reading chat messages
- Deleting and clearing chats

All commands inherit from BaseCommand and provide a consistent interface
for chat-related operations in the Simplex system.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union
from .base import BaseCommand, ChatType, ChatPagination, ItemRange


@dataclass(kw_only=True)
class StartChat(BaseCommand):
    """Command to start a chat session."""

    type: str = "startChat"
    subscribeConnections: bool = False
    enableExpireChatItems: bool = False
    startXFTPWorkers: bool = False


@dataclass(kw_only=True)
class APIStopChat(BaseCommand):
    """Command to stop a chat session via API."""

    type: str = "apiStopChat"


@dataclass(kw_only=True)
class APIGetChats(BaseCommand):
    """Command to get a list of chats via API."""

    type: str = "apiGetChats"
    userId: int
    pendingConnections: bool = False


@dataclass(kw_only=True)
class APIGetChat(BaseCommand):
    """Command to get a specific chat via API."""

    type: str = "apiGetChat"
    chatType: ChatType
    chatId: int
    pagination: ChatPagination
    search: Optional[str] = None


@dataclass(kw_only=True)
class APIChatRead(BaseCommand):
    """Command to mark a chat as read via API."""

    type: str = "apiChatRead"
    chatType: ChatType
    chatId: int
    itemRange: Optional[ItemRange] = None


@dataclass(kw_only=True)
class APIDeleteChat(BaseCommand):
    """Command to delete a chat via API."""

    type: str = "apiDeleteChat"
    chatType: ChatType
    chatId: int


@dataclass(kw_only=True)
class APIClearChat(BaseCommand):
    """Command to clear a chat's messages via API."""

    type: str = "apiClearChat"
    chatType: ChatType
    chatId: int


# Type alias for ChatCommand
ChatCommand = Union[
    StartChat,
    APIStopChat,
    APIGetChats,
    APIGetChat,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
]
