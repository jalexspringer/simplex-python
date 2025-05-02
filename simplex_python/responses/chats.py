"""
Chat-related response types for the Simplex messaging system.

This module defines response types for chat-related operations, including:
- Chat session management (starting, running, stopping)
- Chat retrieval and listing
- Chat item operations
- Chat status updates

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .base import CommandResponse


@dataclass
class ChatStartedResponse(CommandResponse):
    """Response when a chat session is started."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatStartedResponse":
        return cls(type="chatStarted")


@dataclass
class ChatRunningResponse(CommandResponse):
    """Response indicating that a chat session is running."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatRunningResponse":
        return cls(type="chatRunning")


@dataclass
class ChatStoppedResponse(CommandResponse):
    """Response when a chat session is stopped."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatStoppedResponse":
        return cls(type="chatStopped")


@dataclass
class ApiChatsResponse(CommandResponse):
    """Response containing a list of chats for a user."""

    chats: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiChatsResponse":
        return cls(type="apiChats", user=data.get("user"), chats=data.get("chats", []))


@dataclass
class ApiCommandResponse(CommandResponse):
    """Response containing a single chat with its messages."""

    chat: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiCommandResponse":
        return cls(type="apiChat", user=data.get("user"), chat=data.get("chat", {}))


@dataclass
class ChatReadResponse(CommandResponse):
    """Response when a chat is marked as read."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatReadResponse":
        return cls(type="chatRead", user=data.get("user"))


@dataclass
class ChatDeletedResponse(CommandResponse):
    """Response when a chat is deleted."""

    chatInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatDeletedResponse":
        return cls(
            type="chatDeleted", user=data.get("user"), chatInfo=data.get("chatInfo", {})
        )


@dataclass
class ChatClearedResponse(CommandResponse):
    """Response when a chat is cleared."""

    chatInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatClearedResponse":
        return cls(
            type="chatCleared", user=data.get("user"), chatInfo=data.get("chatInfo", {})
        )


@dataclass
class NewChatItemsResponse(CommandResponse):
    """Response containing new chat items."""

    chatItems: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewChatItemsResponse":
        return cls(
            type="newChatItems",
            user=data.get("user"),
            chatItems=data.get("chatItems", []),
        )


@dataclass
class ChatItemUpdatedResponse(CommandResponse):
    """Response when a chat item is updated."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatItemUpdatedResponse":
        return cls(
            type="chatItemUpdated",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
        )


@dataclass
class ChatItemDeletedResponse(CommandResponse):
    """Response when a chat item is deleted."""

    deletedChatItem: Dict[str, Any] = field(default_factory=dict)
    toChatItem: Optional[Dict[str, Any]] = None
    byUser: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatItemDeletedResponse":
        return cls(
            type="chatItemDeleted",
            user=data.get("user"),
            deletedChatItem=data.get("deletedChatItem", {}),
            toChatItem=data.get("toChatItem"),
            byUser=data.get("byUser", False),
        )


@dataclass
class ChatItemStatusUpdatedResponse(CommandResponse):
    """Response when a chat item's status is updated."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatItemStatusUpdatedResponse":
        return cls(
            type="chatItemStatusUpdated",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
        )


# Supporting data classes


@dataclass
class Chat:
    """Chat information with items and stats."""

    chatInfo: Dict[str, Any]
    chatItems: List[Dict[str, Any]]
    chatStats: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chat":
        return cls(
            chatInfo=data.get("chatInfo", {}),
            chatItems=data.get("chatItems", []),
            chatStats=data.get("chatStats", {}),
        )


@dataclass
class ChatStats:
    """Chat statistics."""

    unreadCount: int
    minUnreadItemId: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatStats":
        return cls(
            unreadCount=data.get("unreadCount", 0),
            minUnreadItemId=data.get("minUnreadItemId", 0),
        )
