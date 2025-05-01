"""
User-related commands for the SimpleX protocol.

This module contains command classes for user management including:
- User profile commands
- User account commands
- User settings commands

These commands manage user identities and their settings in the SimpleX system.
"""

from dataclasses import dataclass
from typing import Optional

from .base import BaseCommand, Profile


@dataclass(kw_only=True)
class ShowActiveUser(BaseCommand):
    """Command to show the active user profile.

    Attributes:
        type: Discriminator for this command ("showActiveUser").
    """

    type: str = "showActiveUser"


@dataclass(kw_only=True)
class CreateActiveUser(BaseCommand):
    """Command to create a new active user.

    Attributes:
        type: Discriminator for this command ("createActiveUser").
        profile: Optional profile information for the new user.
        same_servers: Whether to use the same servers as before.
        past_timestamp: Whether to use a past timestamp for creation.
    """

    type: str = "createActiveUser"
    profile: Optional[Profile] = None
    same_servers: bool = True
    past_timestamp: bool = False


@dataclass(kw_only=True)
class ListUsers(BaseCommand):
    """Command to list all users.

    Attributes:
        type: Discriminator for this command ("listUsers").
    """

    type: str = "listUsers"


@dataclass(kw_only=True)
class APISetActiveUser(BaseCommand):
    """Command to set the active user for the API.

    Attributes:
        type: Discriminator for this command ("apiSetActiveUser").
        user_id: The user's unique identifier.
        view_pwd: Optional password required to view the user.
    """

    type: str = "apiSetActiveUser"
    user_id: int
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class APIHideUser(BaseCommand):
    """Command to hide a user in the system.

    Attributes:
        type: Discriminator for this command ("apiHideUser").
        user_id: ID of the user to hide.
        view_pwd: Password required to view the user.
    """

    type: str = "apiHideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIUnhideUser(BaseCommand):
    """Command to unhide a user in the system.

    Attributes:
        type: Discriminator for this command ("apiUnhideUser").
        user_id: ID of the user to unhide.
        view_pwd: Password required to view the user.
    """

    type: str = "apiUnhideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIMuteUser(BaseCommand):
    """Command to mute a user in the system.

    Attributes:
        type: Discriminator for this command ("apiMuteUser").
        user_id: ID of the user to mute.
    """

    type: str = "apiMuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIUnmuteUser(BaseCommand):
    """Command to unmute a user in the system.

    Attributes:
        type: Discriminator for this command ("apiUnmuteUser").
        user_id: ID of the user to unmute.
    """

    type: str = "apiUnmuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIDeleteUser(BaseCommand):
    """Command to delete a user from the system.

    Attributes:
        type: Discriminator for this command ("apiDeleteUser").
        user_id: ID of the user to delete.
        del_smp_queues: Whether to delete SMP queues.
        view_pwd: Optional password required to view the user.
    """

    type: str = "apiDeleteUser"
    user_id: int
    del_smp_queues: bool
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class APIUpdateProfile(BaseCommand):
    """Command to update a user's profile.

    Attributes:
        type: Discriminator for this command ("apiUpdateProfile").
        user_id: The user's unique identifier.
        profile: The new profile object.
    """

    type: str = "apiUpdateProfile"
    user_id: int
    profile: Profile


@dataclass(kw_only=True)
class SetIncognito(BaseCommand):
    """Command to enable or disable incognito mode.

    Attributes:
        type: Discriminator for this command ("setIncognito").
        incognito: Whether to enable incognito mode.
    """

    type: str = "setIncognito"
    incognito: bool


@dataclass(kw_only=True)
class APIGetUserProtoServers(BaseCommand):
    """Command to get the user's protocol servers.

    Attributes:
        type: Discriminator for this command ("apiGetUserProtoServers").
        user_id: The user identifier.
        server_protocol: The server protocol to query.
    """

    type: str = "apiGetUserProtoServers"
    user_id: int
    server_protocol: "ServerProtocol"  # Forward reference to avoid circular import


@dataclass(kw_only=True)
class APISetUserProtoServers(BaseCommand):
    """Command to set the user's protocol servers.

    Attributes:
        type: Discriminator for this command ("apiSetUserProtoServers").
        user_id: The user identifier.
        server_protocol: The server protocol to set.
        servers: List of server configurations.
    """

    type: str = "apiSetUserProtoServers"
    user_id: int
    server_protocol: "ServerProtocol"  # Forward reference to avoid circular import
    servers: list["ServerCfg"]  # Forward reference to avoid circular import


# Update the __all__ list to control what's exported
__all__ = [
    "ShowActiveUser",
    "CreateActiveUser",
    "ListUsers",
    "APISetActiveUser",
    "APIHideUser",
    "APIUnhideUser",
    "APIMuteUser",
    "APIUnmuteUser",
    "APIDeleteUser",
    "APIUpdateProfile",
    "SetIncognito",
    "APIGetUserProtoServers",
    "APISetUserProtoServers",
]
