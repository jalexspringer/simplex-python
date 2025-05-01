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
