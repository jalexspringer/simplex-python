"""
Message-related response types for the Simplex messaging system.

This module defines response types for message-related operations, including:
- Message sending confirmations
- Message update notifications
- Message deletion confirmations
- Message error responses

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from .base import CommandResponse


@dataclass
class MessageSentResponse(CommandResponse):
    """Response when a message is successfully sent."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageSentResponse":
        return cls(
            type="messageSent", user=data.get("user"), chatItem=data.get("chatItem", {})
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
class MessageErrorResponse(CommandResponse):
    """Response when there is an error with a message operation."""

    severity: str = ""
    errorMessage: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageErrorResponse":
        return cls(
            type="messageError",
            user=data.get("user"),
            severity=data.get("severity", ""),
            errorMessage=data.get("errorMessage", ""),
        )


@dataclass
class MsgIntegrityErrorResponse(CommandResponse):
    """Response when there is a message integrity error."""

    msgError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MsgIntegrityErrorResponse":
        return cls(
            type="msgIntegrityError",
            user=data.get("user"),
            msgError=data.get("msgError", {}),
        )


# Type alias for message-related responses
MessageResponse = (
    MessageSentResponse
    | ChatItemUpdatedResponse
    | ChatItemDeletedResponse
    | MessageErrorResponse
    | MsgIntegrityErrorResponse
)
