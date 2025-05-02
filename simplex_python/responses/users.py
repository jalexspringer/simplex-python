"""
User-related response types for the Simplex messaging system.

This module defines response types for user-related operations, including:
- User management (active users, profiles, settings)
- Address management (creation, deletion, display)
- Auto-accept configuration
- Contact link management

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .base import CommandResponse


# User profile and management responses


@dataclass
class ActiveUserResponse(CommandResponse):
    """Response containing active user information."""

    user: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActiveUserResponse":
        return cls(type="activeUser", user=data.get("user", {}))


@dataclass
class UsersListResponse(CommandResponse):
    """Response containing a list of users."""

    users: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsersListResponse":
        return cls(type="usersList", users=data.get("users", []))


@dataclass
class UserProfileResponse(CommandResponse):
    """Response containing a user's profile."""

    profile: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfileResponse":
        return cls(
            type="userProfile", user=data.get("user"), profile=data.get("profile", {})
        )


@dataclass
class UserProfileUpdatedResponse(CommandResponse):
    """Response when a user's profile is updated."""

    fromProfile: Dict[str, Any] = field(default_factory=dict)
    toProfile: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfileUpdatedResponse":
        return cls(
            type="userProfileUpdated",
            user=data.get("user"),
            fromProfile=data.get("fromProfile", {}),
            toProfile=data.get("toProfile", {}),
        )


@dataclass
class UserProfileNoChangeResponse(CommandResponse):
    """Response when a profile update results in no change."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfileNoChangeResponse":
        return cls(type="userProfileNoChange", user=data.get("user"))


# Address-related responses


@dataclass
class UserContactLinkResponse(CommandResponse):
    """Response containing a user's contact link (address)."""

    contactLink: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkResponse":
        return cls(
            type="userContactLink",
            user=data.get("user"),
            contactLink=data.get("contactLink", {}),
        )


@dataclass
class UserContactLinkCreatedResponse(CommandResponse):
    """Response when a user contact link is created."""

    connReqContact: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkCreatedResponse":
        return cls(
            type="userContactLinkCreated",
            user=data.get("user"),
            connReqContact=data.get("connReqContact", ""),
        )


@dataclass
class UserContactLinkDeletedResponse(CommandResponse):
    """Response when a user contact link is deleted."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkDeletedResponse":
        return cls(type="userContactLinkDeleted", user=data.get("user"))


@dataclass
class UserContactLinkUpdatedResponse(CommandResponse):
    """Response when a user's contact link is updated."""

    connReqContact: str = ""
    autoAccept: bool = False
    autoReply: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkUpdatedResponse":
        return cls(
            type="userContactLinkUpdated",
            user=data.get("user"),
            connReqContact=data.get("connReqContact", ""),
            autoAccept=data.get("autoAccept", False),
            autoReply=data.get("autoReply"),
        )


# Supporting data classes and type aliases


@dataclass
class User:
    """User information returned in responses."""

    userId: int
    agentUserId: str
    userContactId: int
    localDisplayName: str
    profile: Dict[str, Any]
    activeUser: bool
    viewPwdHash: str = ""
    showNtfs: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            userId=data.get("userId", 0),
            agentUserId=data.get("agentUserId", ""),
            userContactId=data.get("userContactId", 0),
            localDisplayName=data.get("localDisplayName", ""),
            profile=data.get("profile", {}),
            activeUser=data.get("activeUser", False),
            viewPwdHash=data.get("viewPwdHash", ""),
            showNtfs=data.get("showNtfs", True),
        )


@dataclass
class UserContactLink:
    """User contact link information."""

    connReqContact: str
    autoAccept: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLink":
        return cls(
            connReqContact=data.get("connReqContact", ""),
            autoAccept=data.get("autoAccept"),
        )
