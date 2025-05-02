"""
Enums and constants for the Simplex chat protocol.

This module centralizes constants and enumerations used across the client library.
"""

from enum import Enum
from typing import Literal


class ChatType(Enum):
    """Chat types in Simplex protocol."""
    
    DIRECT = "@"
    GROUP = "#"
    CONTACT_REQUEST = "<@"
    
    @classmethod
    def from_str(cls, chat_type: str) -> "ChatType":
        """Convert string representation to ChatType enum."""
        mapping = {
            "direct": cls.DIRECT,
            "group": cls.GROUP,
            "contact_request": cls.CONTACT_REQUEST,
        }
        return mapping.get(chat_type.lower(), cls.DIRECT)


class MemberRole(Enum):
    """Group member roles."""
    
    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"
    
    @classmethod
    def from_str(cls, role: str) -> "MemberRole":
        """Convert string representation to MemberRole enum."""
        mapping = {
            "member": cls.MEMBER,
            "admin": cls.ADMIN,
            "owner": cls.OWNER,
        }
        return mapping.get(role.lower(), cls.MEMBER)


class DeleteMode(Enum):
    """Message deletion modes."""
    
    LOCAL = "local"
    BROADCAST = "broadcast"


# Common response types for validation
ChatResponseType = Literal[
    "activeUser",
    "apiChats",
    "apiChat",
    "chatItemUpdated",
    "newChatItems",
    "userContactLinkShown",
    "userContactLinkCreated",
    "userContactLinkDeleted",
    "incognitoUpdated",
    "userContactLinkUpdated",
    "groupCreated",
    "memberAdded",
    "memberRemoved",
    "leftGroup",
    "groupMembers",
    "groupProfileUpdated",
    "groupLinkCreated",
    "fileSent",
    "fileReceived",
]
