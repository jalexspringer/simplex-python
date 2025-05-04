"""
Base response types for the Simplex messaging system.

This module defines the foundation for all response types in the SDK:
- Core response base class (CommandResponse)
- Response error types
- Common utilities and shared data structures

Note on terminology: In the Simplex system, 'Chat' has two meanings:
1. A conversation thread containing messages ('chat items')
2. The overall application name (e.g., in 'ChatCmd' which refers to any command sent to the application)

For clarity, we use 'Command' prefix for application-level concepts and 'Chat' prefix
for conversation-related concepts, even though the upstream API uses 'Chat' for both.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


# Base response structure - all responses will be parsed into this
@dataclass
class CommandResponse:
    """Base class for all command responses."""

    type: str
    user: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandResponse":
        """Create a CommandResponse from a dictionary."""
        if not isinstance(data, dict):
            return CommandResponse(type="unknown")

        response_type = data.get("type", "unknown")

        # For generic/unknown response types, just create a basic response
        return CommandResponse(type=response_type, user=data.get("user"))


# Chat types - used across different domain responses
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


# Error responses
@dataclass
class CommandErrorResponse(CommandResponse):
    """Response when a command results in an error."""

    commandError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandErrorResponse":
        return cls(
            type="chatCmdError",  # Keep original API type while using clearer class name
            user=data.get("user"),
            commandError=data.get("chatError", {}),  # Map from original API field name
        )


# Error types
@dataclass
class CommandError:
    """Base class for command errors."""

    type: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CommandError":
        error_type = data.get("type")

        if error_type == "error":
            return CommandErrorType.from_dict(data)
        elif error_type == "errorAgent":
            return AgentErrorType.from_dict(data)
        elif error_type == "errorStore":
            return StoreErrorType.from_dict(data)

        return CommandError(type=error_type)


@dataclass
class CommandErrorType(CommandError):
    """Command protocol error."""

    errorType: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandErrorType":
        return cls(type="error", errorType=data.get("errorType", {}))


@dataclass
class AgentErrorType(CommandError):
    """Agent-level error."""

    agentError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentErrorType":
        return cls(type="errorAgent", agentError=data.get("agentError", {}))


@dataclass
class StoreErrorType(CommandError):
    """Storage-related error."""

    storeError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoreErrorType":
        return cls(type="errorStore", storeError=data.get("storeError", {}))


@dataclass
class CmdOkResponse(CommandResponse):
    """Response when a command succeeds with no specific return data."""

    user_: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CmdOkResponse":
        return cls(type="cmdOk", user_=data.get("user_"))


@dataclass
class ApiParsedMarkdownResponse(CommandResponse):
    """Response containing parsed and formatted markdown text."""

    formattedText: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiParsedMarkdownResponse":
        return cls(type="apiParsedMarkdown", formattedText=data.get("formattedText"))


class ResponseFactory:
    """
    Factory class for creating appropriate response objects based on response type.
    
    This centralized factory handles the mapping between server response types and
    the corresponding Python response classes.
    """
    
    # This map will be populated by register_response_type
    _response_map: Dict[str, Any] = {}
    
    @classmethod
    def register_response_type(cls, response_type: str, response_class: Any) -> None:
        """
        Register a response type with its corresponding class.
        
        Args:
            response_type: The response type string (e.g., "activeUser")
            response_class: The corresponding response class
        """
        cls._response_map[response_type] = response_class
    
    @classmethod
    def create(cls, data: Dict[str, Any]) -> CommandResponse:
        """
        Create a response object of the appropriate type based on the response data.
        
        Args:
            data: The response data dictionary
            
        Returns:
            An instance of the appropriate CommandResponse subclass
        """
        if not isinstance(data, dict):
            return CommandResponse(type="unknown")
            
        response_type = data.get("type", "unknown")
        
        # Handle error responses
        if response_type == "chatCmdError":
            return CommandErrorResponse.from_dict(data)
        
        # Check if we have a registered handler for this response type
        if response_type in cls._response_map:
            try:
                return cls._response_map[response_type].from_dict(data)
            except Exception as e:
                # If there's an error creating the specific response, log it and fall back
                import logging
                logging.getLogger(__name__).error(
                    f"Error creating response for type {response_type}: {e}"
                )
        
        # Fall back to generic response
        return CommandResponse(type=response_type, user=data.get("user"))
