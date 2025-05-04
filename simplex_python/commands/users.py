"""
User and address-related command classes for the Simplex messaging system.

This module defines the commands for managing users and addresses, including:
- User management (creating, listing, activating, hiding, muting, etc.)
- User profile operations
- Address creation and management
- Address auto-accept configuration

All commands inherit from BaseCommand and provide a consistent interface
for user-related operations in the Simplex system.
"""

from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
from .base import BaseCommand, MsgContent


# User-related command classes


@dataclass(kw_only=True)
class ShowActiveUser(BaseCommand):
    """Command to show the currently active user."""

    type: str = "showActiveUser"


@dataclass(kw_only=True)
class CreateActiveUser(BaseCommand):
    """Command to create a new user profile and set it as active."""

    type: str = "createActiveUser"
    profile: Optional["Profile"] = None
    sameServers: bool = True
    pastTimestamp: bool = False


@dataclass(kw_only=True)
class ListUsers(BaseCommand):
    """Command to list all users."""

    type: str = "listUsers"


@dataclass(kw_only=True)
class APISetActiveUser(BaseCommand):
    """Command to set the active user via API."""

    type: str = "apiSetActiveUser"
    userId: int
    viewPwd: Optional[str] = None


@dataclass(kw_only=True)
class APIHideUser(BaseCommand):
    """Command to hide a user via API."""

    type: str = "apiHideUser"
    userId: int
    viewPwd: str


@dataclass(kw_only=True)
class APIUnhideUser(BaseCommand):
    """Command to unhide a user via API."""

    type: str = "apiUnhideUser"
    userId: int
    viewPwd: str


@dataclass(kw_only=True)
class APIMuteUser(BaseCommand):
    """Command to mute a user via API."""

    type: str = "apiMuteUser"
    userId: int


@dataclass(kw_only=True)
class APIUnmuteUser(BaseCommand):
    """Command to unmute a user via API."""

    type: str = "apiUnmuteUser"
    userId: int


@dataclass(kw_only=True)
class APIDeleteUser(BaseCommand):
    """Command to delete a user via API."""

    type: str = "apiDeleteUser"
    userId: int
    delSMPQueues: bool
    viewPwd: Optional[str] = None


@dataclass(kw_only=True)
class APIUpdateProfile(BaseCommand):
    """Command to update a user's profile via API."""

    type: str = "apiUpdateProfile"
    userId: int
    profile: "Profile"


# Address-related commands (user-related)


@dataclass(kw_only=True)
class CreateMyAddress(BaseCommand):
    """Command to create a new address for the current user."""

    type: str = "createMyAddress"


@dataclass(kw_only=True)
class DeleteMyAddress(BaseCommand):
    """Command to delete the address of the current user."""

    type: str = "deleteMyAddress"


@dataclass(kw_only=True)
class ShowMyAddress(BaseCommand):
    """Command to show the address of the current user."""

    type: str = "showMyAddress"


@dataclass(kw_only=True)
class SetProfileAddress(BaseCommand):
    """Command to set whether to include the address in the user's profile."""

    type: str = "setProfileAddress"
    includeInProfile: bool


@dataclass(kw_only=True)
class AddressAutoAccept(BaseCommand):
    """Command to configure auto-accept settings for the user's address."""

    type: str = "addressAutoAccept"
    autoAccept: Optional["AutoAccept"] = None


@dataclass(kw_only=True)
class APICreateMyAddress(BaseCommand):
    """Command to create a new address for a specific user via API."""

    type: str = "apiCreateMyAddress"
    userId: int


@dataclass(kw_only=True)
class APIDeleteMyAddress(BaseCommand):
    """Command to delete the address of a specific user via API."""

    type: str = "apiDeleteMyAddress"
    userId: int


@dataclass(kw_only=True)
class APIShowMyAddress(BaseCommand):
    """Command to show the address of a specific user via API."""

    type: str = "apiShowMyAddress"
    userId: int


@dataclass(kw_only=True)
class APISetProfileAddress(BaseCommand):
    """Command to set whether to include the address in a specific user's profile via API."""

    type: str = "apiSetProfileAddress"
    userId: int
    includeInProfile: bool


@dataclass(kw_only=True)
class APIAddressAutoAccept(BaseCommand):
    """Command to configure auto-accept settings for a specific user's address via API."""

    type: str = "apiAddressAutoAccept"
    userId: int
    autoAccept: Optional["AutoAccept"] = None


# Supporting data classes for user-related commands


@dataclass
class Profile:
    """User profile information."""

    displayName: str
    fullName: str
    image: Optional[str] = None
    contactLink: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to a dictionary for serialization."""
        return {
            "displayName": self.displayName,
            "fullName": self.fullName,
            **({"image": self.image} if self.image is not None else {}),
            **({"contactLink": self.contactLink} if self.contactLink is not None else {})
        }


@dataclass
class LocalProfile:
    """User profile with local information."""

    profileId: int
    displayName: str
    fullName: str
    localAlias: str
    image: Optional[str] = None
    contactLink: Optional[str] = None


@dataclass
class AutoAccept:
    """Configuration for automatically accepting connection requests."""

    acceptIncognito: bool
    autoReply: Optional[MsgContent] = None


# Type alias for UserCommand
UserCommand = Union[
    ShowActiveUser,
    CreateActiveUser,
    ListUsers,
    APISetActiveUser,
    APIHideUser,
    APIUnhideUser,
    APIMuteUser,
    APIUnmuteUser,
    APIDeleteUser,
    APIUpdateProfile,
    CreateMyAddress,
    DeleteMyAddress,
    ShowMyAddress,
    SetProfileAddress,
    AddressAutoAccept,
    APICreateMyAddress,
    APIDeleteMyAddress,
    APIShowMyAddress,
    APISetProfileAddress,
    APIAddressAutoAccept,
]
