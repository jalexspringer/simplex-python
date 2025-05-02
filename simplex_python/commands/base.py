"""
Base types, enums, and common structures for Simplex commands.

This module defines the core components used by all command types:
- Base command interfaces
- Enumerations used across the command system
- Common data structures shared by multiple commands

All commands in the Simplex system should inherit from these base structures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


@dataclass
class BaseCommand:
    """Base class for all chat commands.

    All command classes inherit from this base class and should be
    convertible to a string command via the command_formatting.py utilities.

    Attributes:
        type: A required string field that identifies the command type.
              All subclasses must define this field with a specific value.
              This attribute is used by the cmd_string function to determine
              the appropriate string representation of the command.

    Example:
        @dataclass
        class ShowActiveUser(BaseCommand):
            type: str = "showActiveUser"
    """

    type: str

    def to_cmd_string(self):
        """Convert command to string format.

        This method delegates to the cmd_string function in command_formatting.py.

        Returns:
            str: The string representation of this command for the API.

        Raises:
            AttributeError: If the required 'type' attribute is not defined.
        """
        from .command_formatting import cmd_string

        return cmd_string(self)


# Shared enums used across different command types
class ChatType(str, Enum):
    """Type of chat."""

    DIRECT = "@"
    GROUP = "#"
    CONTACT_REQUEST = "<@"


class DeleteMode(str, Enum):
    """Deletion mode for chat items."""

    BROADCAST = "broadcast"
    INTERNAL = "internal"


class ServerProtocol(str, Enum):
    """Protocol for server communication."""

    SMP = "smp"
    XFTP = "xftp"


class GroupMemberRole(str, Enum):
    """Role of a member in a group."""

    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"


# Shared type definitions
ChatItemId = int


@dataclass
class ChatPagination:
    """Pagination for chat items."""

    count: int
    after: Optional[ChatItemId] = None
    before: Optional[ChatItemId] = None


@dataclass
class ItemRange:
    """Range of chat items."""

    fromItem: ChatItemId
    toItem: ChatItemId


@dataclass
class ServerCfg:
    """Server configuration."""

    server: str
    preset: bool
    enabled: bool
    tested: Optional[bool] = None


# Common content types
class MsgContentTag(str, Enum):
    """Message content type tag."""

    TEXT = "text"
    LINK = "link"
    IMAGE = "image"
    FILE = "file"


@dataclass
class LinkPreview:
    """Preview for a link in a message."""

    uri: str
    title: str
    description: str
    image: str


@dataclass
class MCBase:
    """Base class for message content."""

    text: str
    type: str


@dataclass
class MCText(MCBase):
    """Text message content."""

    text: str
    type: str = MsgContentTag.TEXT


@dataclass
class MCLink(MCBase):
    """Link message content."""

    text: str
    type: str = MsgContentTag.LINK
    preview: LinkPreview = field(default_factory=LinkPreview)


@dataclass
class MCImage(MCBase):
    """Image message content."""

    text: str
    type: str = MsgContentTag.IMAGE
    image: str = ""  # image preview as base64 encoded data string


@dataclass
class MCFile(MCBase):
    """File message content."""

    text: str
    type: str = MsgContentTag.FILE


@dataclass
class MCUnknown(MCBase):
    """Unknown message content type."""

    text: str
    type: str = field(default="unknown")


# Type alias for message content
MsgContent = Union[MCText, MCLink, MCImage, MCFile, MCUnknown]
