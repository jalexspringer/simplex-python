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

    # Store original user dict for backward compatibility
    user: Dict[str, Any] = field(default_factory=dict)

    # Directly expose common user properties for fluent API
    user_id: Optional[int] = None
    agent_user_id: Optional[str] = None
    local_display_name: Optional[str] = None
    profile: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActiveUserResponse":
        user_data = data.get("user", {})

        # Create the response with both the original user dict and extracted properties
        return cls(
            type="activeUser",
            user=user_data,
            user_id=user_data.get("userId"),
            agent_user_id=user_data.get("agentUserId"),
            local_display_name=user_data.get("localDisplayName"),
            profile=user_data.get("profile", {}),
            preferences=user_data.get("fullPreferences", {}),
        )

    @property
    def display_name(self) -> Optional[str]:
        """Get the user's display name from profile."""
        return self.profile.get("displayName") if self.profile else None

    @property
    def full_name(self) -> Optional[str]:
        """Get the user's full name from profile."""
        return self.profile.get("fullName") if self.profile else None

    @property
    def profile_address(self) -> Optional[str]:
        """Get the user's profile address (contact link) if it exists."""

        return self.profile.get("contactLink")

    @property
    def has_profile_address(self) -> bool:
        """Check if the user has a profile address."""
        return "contactLink" in self.profile and self.profile["contactLink"] is not None


@dataclass
class UsersListResponse(CommandResponse):
    """Response containing a list of users."""

    users: List[Dict[str, Any]] = field(default_factory=list)

    # Internal representation of processed user items
    _user_items: List["UserItem"] = field(default_factory=list, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsersListResponse":
        raw_users = data.get("users", [])
        response = cls(type="usersList", users=raw_users)

        # Process raw users into UserItem objects
        response._user_items = [
            UserItem.from_dict(user_data) for user_data in raw_users
        ]
        return response

    def __len__(self) -> int:
        """Return the number of users in the list."""
        return len(self._user_items)

    def __getitem__(self, index) -> "UserItem":
        """Access user items by index."""
        return self._user_items[index]

    def __iter__(self):
        """Allow iteration over user items."""
        return iter(self._user_items)


@dataclass
class UserItem:
    """Individual user item from a users list response."""

    # Raw user dictionary
    user: Dict[str, Any] = field(default_factory=dict)

    # Direct access to common properties
    user_id: Optional[int] = None
    agent_user_id: Optional[str] = None
    local_display_name: Optional[str] = None
    profile: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    active_user: bool = False
    unread_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserItem":
        """Create a UserItem from a dictionary."""
        user_data = data.get("user", {})

        return cls(
            user=user_data,
            user_id=user_data.get("userId"),
            agent_user_id=user_data.get("agentUserId"),
            local_display_name=user_data.get("localDisplayName"),
            profile=user_data.get("profile", {}),
            preferences=user_data.get("fullPreferences", {}),
            active_user=user_data.get("activeUser", False),
            unread_count=data.get("unreadCount", 0),
        )

    @property
    def display_name(self) -> Optional[str]:
        """Get the user's display name from profile."""
        return self.profile.get("displayName") if self.profile else None

    @property
    def full_name(self) -> Optional[str]:
        """Get the user's full name from profile."""
        return self.profile.get("fullName") if self.profile else None


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


# User contact link subscription responses


@dataclass
class UserContactLinkSubscribedResponse(CommandResponse):
    """Response when a user contact link is subscribed to."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkSubscribedResponse":
        return cls(type="userContactLinkSubscribed")


@dataclass
class UserContactLinkSubErrorResponse(CommandResponse):
    """Response when there's an error with a user contact link subscription."""

    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContactLinkSubErrorResponse":
        return cls(type="userContactLinkSubError", chatError=data.get("chatError", {}))


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
