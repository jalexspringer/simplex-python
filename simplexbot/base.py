"""
Base types, enums, and common structures for Simplex commands.

This module defines the core components used by all command types:
- Base command interfaces
- Enumerations used across the command system
- Common data structures shared by multiple commands

All commands in the Simplex system should inherit from these base structures.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Optional, Dict, Any, Union, runtime_checkable


class ChatType(Enum):
    """Enumeration of chat types.

    Attributes:
        DIRECT: Direct (one-to-one) chat.
        GROUP: Group chat.
        CONTACT_REQUEST: Contact request chat.
    """

    DIRECT = "@"
    GROUP = "#"
    CONTACT_REQUEST = "<@"


class DeleteMode(Enum):
    """Enumeration of chat item deletion modes.

    Attributes:
        BROADCAST: Delete for all participants (broadcast).
        INTERNAL: Delete only locally (internal).
    """

    BROADCAST = "broadcast"
    INTERNAL = "internal"


class GroupMemberRole(Enum):
    """Enumeration of group member roles.

    Attributes:
        MEMBER: Regular group member.
        ADMIN: Group administrator.
        OWNER: Group owner.
    """

    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"


class ServerProtocol(Enum):
    """Enumeration of server protocols.

    Attributes:
        SMP: SimpleX Messaging Protocol
        XFTP: SimpleX File Transfer Protocol
    """

    SMP = "smp"
    XFTP = "xftp"


@runtime_checkable
class Command(Protocol):
    """Protocol defining the basic interface of all command objects.

    All command classes should have a type property that identifies the command.
    """

    type: str


@dataclass(kw_only=True)
class BaseCommand(ABC):
    """Abstract base class for all command objects.

    This class provides common functionality for all commands and ensures
    they conform to the Command protocol.

    Attributes:
        type: String identifier for the command type.
    """

    type: str


@dataclass(kw_only=True)
class Profile:
    """User profile information.

    Attributes:
        display_name: The user's display name.
        full_name: The user's full name.
        image: Optional URL/path to the user's avatar image.
        contact_link: Optional contact link for the user.
    """

    display_name: str
    full_name: str
    image: Optional[str] = None
    contact_link: Optional[str] = None


@dataclass(kw_only=True)
class LocalProfile:
    """User profile information with local settings.

    Attributes:
        profile_id: The profile identifier.
        display_name: The user's display name.
        full_name: The user's full name.
        image: Optional URL/path to the user's avatar image.
        contact_link: Optional contact link for the user.
        local_alias: Local alias for the profile.
    """

    profile_id: int
    display_name: str
    full_name: str
    image: Optional[str] = None
    contact_link: Optional[str] = None
    local_alias: str


@dataclass(kw_only=True)
class GroupProfile:
    """Profile for a group chat.

    Attributes:
        display_name: Display name for the group.
        full_name: Full name for the group.
        image: Optional group image URL or path.
    """

    display_name: str
    full_name: str
    image: Optional[str] = None


@dataclass(kw_only=True)
class ServerCfg:
    """Server configuration.

    Attributes:
        server: Server address.
        preset: Whether this is a preset server.
        tested: Whether this server has been tested.
        enabled: Whether this server is enabled.
    """

    server: str
    preset: bool
    enabled: bool
    tested: Optional[bool] = None


@dataclass(kw_only=True)
class ChatPagination:
    """Pagination parameters for chat queries.

    Attributes:
        count: Number of items to retrieve.
        after: Optional ID to start after.
        before: Optional ID to end before.
    """

    count: int
    after: Optional[int] = None
    before: Optional[int] = None


@dataclass(kw_only=True)
class ItemRange:
    """Range of chat items.

    Attributes:
        from_item: Starting item ID.
        to_item: Ending item ID.
    """

    from_item: int
    to_item: int


@dataclass(kw_only=True)
class ArchiveConfig:
    """Configuration for chat archive import/export.

    Attributes:
        archive_path: Path to the archive file.
        disable_compression: Whether to disable compression.
        parent_temp_directory: Parent directory for temporary files.
    """

    archive_path: str
    disable_compression: Optional[bool] = None
    parent_temp_directory: Optional[str] = None


@dataclass(kw_only=True)
class AutoAccept:
    """Auto-accept configuration for incoming connections.

    Attributes:
        accept_incognito: Whether to accept incognito connections.
        auto_reply: Optional automatic reply message content.
    """

    accept_incognito: bool
    auto_reply: Optional[Dict[str, Any]] = None


# Message content types


@dataclass(kw_only=True)
class LinkPreview:
    """Preview information for a link.

    Attributes:
        uri: Link URI.
        title: Link title.
        description: Link description.
        image: Link preview image.
    """

    uri: str
    title: str
    description: str
    image: str


@dataclass(kw_only=True)
class MCText:
    """Text message content.

    Attributes:
        type: Message content type ("text").
        text: The text content.
    """

    type: str = "text"
    text: str


@dataclass(kw_only=True)
class MCLink:
    """Link message content.

    Attributes:
        type: Message content type ("link").
        text: The text content.
        preview: Link preview information.
    """

    type: str = "link"
    text: str
    preview: LinkPreview


@dataclass(kw_only=True)
class MCImage:
    """Image message content.

    Attributes:
        type: Message content type ("image").
        text: The text content.
        image: Image data as base64 encoded string.
    """

    type: str = "image"
    text: str
    image: str


@dataclass(kw_only=True)
class MCFile:
    """File message content.

    Attributes:
        type: Message content type ("file").
        text: The file description or name.
    """

    type: str = "file"
    text: str


@dataclass(kw_only=True)
class MCUnknown:
    """Unknown message content type.

    Attributes:
        type: Message content type (unknown string).
        text: The text content.
    """

    type: str
    text: str


# Define the union type for message content
MsgContent = Union[MCText, MCLink, MCImage, MCFile, MCUnknown]


@dataclass(kw_only=True)
class ComposedMessage:
    """Composed message object for sending.

    Attributes:
        msg_content: The message content object.
        file_path: Optional file path to attach.
        quoted_item_id: Optional ID of quoted chat item.
    """

    msg_content: MsgContent
    file_path: Optional[str] = None
    quoted_item_id: Optional[int] = None
