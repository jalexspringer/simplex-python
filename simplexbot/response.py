"""
Response dataclasses and supporting types for the Simplex Python client.

This module defines Python dataclasses mirroring the TypeScript response types from the Simplex chat client.
Each response is represented as a dataclass with type hints and Google-style docstrings, suitable for use
with the Simplex WebSocket API.

All types follow Python 3.13+ idioms and best practices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .command import Profile  # Import additional types as needed


@dataclass(kw_only=True)
class CRActiveUser:
    """Response for the currently active user.

    Attributes:
        type: Discriminator for this response type ("activeUser").
        user: The active user's profile or identifier.
    """

    type: str = "activeUser"
    user: Profile  # Replace with actual User type when defined


@dataclass(kw_only=True)
class CRUsersList:
    """Response containing a list of users.

    Attributes:
        type: Discriminator for this response type ("usersList").
        users: List of user profiles or identifiers.
    """

    type: str = "usersList"
    users: List[Profile]  # Replace with actual UserInfo type when defined


@dataclass(kw_only=True)
class CRChatStarted:
    """Response indicating a chat has started.

    Attributes:
        type: Discriminator for this response type ("chatStarted").
    """

    type: str = "chatStarted"


@dataclass(kw_only=True)
class CRChatRunning:
    """Response indicating a chat is running.

    Attributes:
        type: Discriminator for this response type ("chatRunning").
    """

    type: str = "chatRunning"


@dataclass(kw_only=True)
class CRChatStopped:
    """Response indicating a chat has stopped.

    Attributes:
        type: Discriminator for this response type ("chatStopped").
    """

    type: str = "chatStopped"


@dataclass(kw_only=True)
class CRApiChats:
    """Response containing user and chat list.

    Attributes:
        type: Discriminator for this response type ("apiChats").
        user: The user associated with these chats.
        chats: List of chat objects.
    """

    type: str = "apiChats"
    user: Profile  # Replace with User when defined
    chats: list  # Replace with List[Chat] when Chat is defined


@dataclass(kw_only=True)
class CRApiChat:
    """Response containing a single chat for a user.

    Attributes:
        type: Discriminator for this response type ("apiChat").
        user: The user associated with the chat.
        chat: The chat object.
    """

    type: str = "apiChat"
    user: Profile  # Replace with User when defined
    chat: object  # Replace with Chat when defined


@dataclass(kw_only=True)
class CRApiParsedMarkdown:
    """Response containing parsed markdown as formatted text.

    Attributes:
        type: Discriminator for this response type ("apiParsedMarkdown").
        formatted_text: Optional list of formatted text objects.
    """

    type: str = "apiParsedMarkdown"
    formatted_text: Optional[list] = None  # Replace with Optional[List[FormattedText]]


@dataclass(kw_only=True)
class CRUserProtoServers:
    """Response containing user and protocol servers info.

    Attributes:
        type: Discriminator for this response type ("userProtoServers").
        user: The user associated with these servers.
        servers: The protocol servers info.
    """

    type: str = "userProtoServers"
    user: Profile  # Replace with User when defined
    servers: object  # Replace with UserProtoServers when defined


@dataclass(kw_only=True)
class CRContactInfo:
    """Response containing contact info for a user.

    Attributes:
        type: Discriminator for this response type ("contactInfo").
        user: The user associated with the contact.
        contact: The contact object.
        connection_stats: The connection stats object.
        custom_user_profile: Optional custom profile for the user.
    """

    type: str = "contactInfo"
    user: Profile  # Replace with User when defined
    contact: object  # Replace with Contact when defined
    connection_stats: object  # Replace with ConnectionStats when defined
    custom_user_profile: Optional[Profile] = None


@dataclass(kw_only=True)
class CRNewChatItems:
    """Response containing new chat items for a user.

    Attributes:
        type: Discriminator for this response type ("newChatItems").
        user: The user receiving new chat items.
        chat_items: List of chat items.
    """

    type: str = "newChatItems"
    user: Profile  # Replace with User when defined
    chat_items: list  # Replace with List[AChatItem] when defined


@dataclass(kw_only=True)
class CRChatItemStatusUpdated:
    """Response indicating a chat item's status was updated.

    Attributes:
        type: Discriminator for this response type ("chatItemStatusUpdated").
        user: The user associated with the chat item.
        chat_item: The chat item object.
    """

    type: str = "chatItemStatusUpdated"
    user: Profile  # Replace with User when defined
    chat_item: object  # Replace with AChatItem when defined


@dataclass(kw_only=True)
class CRChatItemUpdated:
    """Response indicating a chat item was updated.

    Attributes:
        type: Discriminator for this response type ("chatItemUpdated").
        user: The user associated with the chat item.
        chat_item: The chat item object.
    """

    type: str = "chatItemUpdated"
    user: Profile  # Replace with User when defined
    chat_item: object  # Replace with AChatItem when defined


@dataclass(kw_only=True)
class CRChatItemDeleted:
    """Response indicating a chat item was deleted.

    Attributes:
        type: Discriminator for this response type ("chatItemDeleted").
        user: The user associated with the deleted chat item.
        deleted_chat_item: The deleted chat item object.
        to_chat_item: Optional new chat item object.
        by_user: Whether the deletion was by the user.
    """

    type: str = "chatItemDeleted"
    user: Profile  # Replace with User when defined
    deleted_chat_item: object  # Replace with AChatItem when defined
    to_chat_item: object = None  # Replace with Optional[AChatItem]
    by_user: bool = False


@dataclass(kw_only=True)
class CRMsgIntegrityError:
    """Response indicating a message integrity error.

    Attributes:
        type: Discriminator for this response type ("msgIntegrityError").
        user: The user associated with the message error.
        msg_error: The message error type.
    """

    type: str = "msgIntegrityError"
    user: Profile  # Replace with User when defined
    msg_error: object  # Replace with MsgErrorType when defined


@dataclass(kw_only=True)
class CRCmdOk:
    """Response indicating a command succeeded.

    Attributes:
        type: Discriminator for this response type ("cmdOk").
        user: Optional user associated with the command.
    """

    type: str = "cmdOk"
    user_: Profile = None  # Replace with Optional[User] when defined
