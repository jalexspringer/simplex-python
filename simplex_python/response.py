"""
Response type definitions for the Simplex messaging system.

This module defines the response types returned from the chat server,
providing type hints and structure for properly handling server responses.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


# Basic response structure - all responses will be parsed into this
@dataclass
class ChatResponse:
    """Base class for all chat responses."""

    type: str
    user: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatResponse":
        """Create a ChatResponse from a dictionary."""
        if not isinstance(data, dict):
            return ChatResponse(type="unknown")

        response_type = data.get("type", "unknown")

        # Handle known response types with specific parsing
        if response_type == "activeUser":
            return ActiveUserResponse.from_dict(data)
        elif response_type == "apiChats":
            return ApiChatsResponse.from_dict(data)
        elif response_type == "apiChat":
            return ApiChatResponse.from_dict(data)
        elif response_type == "newChatItems":
            return NewChatItemsResponse.from_dict(data)
        elif response_type == "chatItemDeleted":
            return ChatItemDeletedResponse.from_dict(data)
        elif response_type == "contactConnected":
            return ContactConnectedResponse.from_dict(data)
        elif response_type == "chatCmdError":
            return ChatCmdErrorResponse.from_dict(data)

        # For other response types, just create a generic response
        return ChatResponse(type=response_type, user=data.get("user"))


# Chat types
class ChatInfoType(str, Enum):
    """Type of chat"""

    DIRECT = "direct"
    GROUP = "group"
    CONTACT_REQUEST = "contactRequest"


@dataclass
class ChatInfo:
    """Information about a chat."""

    type: ChatInfoType

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChatInfo":
        """Create a ChatInfo from a dictionary."""
        chat_type = data.get("type")

        if chat_type == ChatInfoType.DIRECT:
            return DirectChatInfo.from_dict(data)
        elif chat_type == ChatInfoType.GROUP:
            return GroupChatInfo.from_dict(data)
        elif chat_type == ChatInfoType.CONTACT_REQUEST:
            return ContactRequestChatInfo.from_dict(data)

        # Default fallback
        return ChatInfo(type=chat_type)


@dataclass
class DirectChatInfo(ChatInfo):
    """Direct chat information."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DirectChatInfo":
        return cls(type=ChatInfoType.DIRECT, contact=data.get("contact", {}))


@dataclass
class GroupChatInfo(ChatInfo):
    """Group chat information."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupChatInfo":
        return cls(type=ChatInfoType.GROUP, groupInfo=data.get("groupInfo", {}))


@dataclass
class ContactRequestChatInfo(ChatInfo):
    """Contact request chat information."""

    contactRequest: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactRequestChatInfo":
        return cls(
            type=ChatInfoType.CONTACT_REQUEST,
            contactRequest=data.get("contactRequest", {}),
        )


# Chat item components
@dataclass
class ChatItem:
    """A chat item (message)."""

    chatDir: Dict[str, Any]
    meta: Dict[str, Any]
    content: Dict[str, Any]
    formattedText: Optional[List[Dict[str, Any]]] = None
    quotedItem: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatItem":
        return cls(
            chatDir=data.get("chatDir", {}),
            meta=data.get("meta", {}),
            content=data.get("content", {}),
            formattedText=data.get("formattedText"),
            quotedItem=data.get("quotedItem"),
        )


@dataclass
class AChatItem:
    """A chat item with its chat info."""

    chatInfo: ChatInfo
    chatItem: ChatItem

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AChatItem":
        return cls(
            chatInfo=ChatInfo.from_dict(data.get("chatInfo", {})),
            chatItem=ChatItem.from_dict(data.get("chatItem", {})),
        )


# Specific response types
@dataclass
class ActiveUserResponse(ChatResponse):
    """Response containing active user information."""

    user: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActiveUserResponse":
        return cls(type="activeUser", user=data.get("user", {}))


@dataclass
class ApiChatsResponse(ChatResponse):
    """Response listing chats for a user."""

    chats: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiChatsResponse":
        return cls(type="apiChats", user=data.get("user"), chats=data.get("chats", []))


@dataclass
class ApiChatResponse(ChatResponse):
    """Response containing a single chat with its messages."""

    chat: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiChatResponse":
        return cls(type="apiChat", user=data.get("user"), chat=data.get("chat", {}))


@dataclass
class NewChatItemsResponse(ChatResponse):
    """Response containing new chat items."""

    chatItems: List[AChatItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NewChatItemsResponse":
        chat_items_raw = data.get("chatItems", [])
        chat_items = [AChatItem.from_dict(item) for item in chat_items_raw]

        return cls(type="newChatItems", user=data.get("user"), chatItems=chat_items)


@dataclass
class ChatItemDeletedResponse(ChatResponse):
    """Response when a chat item is deleted."""

    deletedChatItem: AChatItem = field(
        default_factory=lambda: AChatItem(
            ChatInfo(type="unknown"), ChatItem({}, {}, {})
        )
    )
    toChatItem: Optional[AChatItem] = None
    byUser: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatItemDeletedResponse":
        deleted_item = data.get("deletedChatItem", {})
        to_item = data.get("toChatItem")

        return cls(
            type="chatItemDeleted",
            user=data.get("user"),
            deletedChatItem=AChatItem.from_dict(deleted_item) if deleted_item else None,
            toChatItem=AChatItem.from_dict(to_item) if to_item else None,
            byUser=data.get("byUser", False),
        )


@dataclass
class ContactConnectedResponse(ChatResponse):
    """Response when a contact connection is established."""

    contact: Dict[str, Any] = field(default_factory=dict)
    userCustomProfile: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactConnectedResponse":
        return cls(
            type="contactConnected",
            user=data.get("user"),
            contact=data.get("contact", {}),
            userCustomProfile=data.get("userCustomProfile"),
        )


@dataclass
class ChatCmdErrorResponse(ChatResponse):
    """Response when a command results in an error."""

    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatCmdErrorResponse":
        return cls(
            type="chatCmdError",
            user=data.get("user"),
            chatError=data.get("chatError", {}),
        )


# Error types
@dataclass
class ChatError:
    """Base class for chat errors."""

    type: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChatError":
        error_type = data.get("type")

        if error_type == "error":
            return ChatErrorType.from_dict(data)
        elif error_type == "errorAgent":
            return AgentErrorType.from_dict(data)
        elif error_type == "errorStore":
            return StoreErrorType.from_dict(data)

        return ChatError(type=error_type)


@dataclass
class ChatErrorType(ChatError):
    """Chat protocol error."""

    errorType: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatErrorType":
        return cls(type="error", errorType=data.get("errorType", {}))


@dataclass
class AgentErrorType(ChatError):
    """Agent-level error."""

    agentError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentErrorType":
        return cls(type="errorAgent", agentError=data.get("agentError", {}))


@dataclass
class StoreErrorType(ChatError):
    """Storage-related error."""

    storeError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoreErrorType":
        return cls(type="errorStore", storeError=data.get("storeError", {}))
