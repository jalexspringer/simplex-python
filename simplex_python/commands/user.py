"""
User management commands for Simplex messaging system.

This module defines command classes for user management operations:
- Creating and managing user profiles
- User visibility and permissions
- User authentication
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseCommand, Profile


@dataclass(kw_only=True)
class ShowActiveUser(BaseCommand):
    """Command to show the active user profile.

    Attributes:
        type: Command type identifier ("showActiveUser").
    """

    type: str = "showActiveUser"


@dataclass(kw_only=True)
class CreateActiveUser(BaseCommand):
    """Command to create a new user profile and set it as active.

    Attributes:
        type: Command type identifier ("createActiveUser").
        profile: Optional user profile information.
        same_servers: Whether to use the same servers as existing users.
        past_timestamp: Whether to set the creation timestamp in the past.
    """

    type: str = "createActiveUser"
    profile: Optional[Profile] = None
    same_servers: bool = True
    past_timestamp: bool = False


@dataclass(kw_only=True)
class ListUsers(BaseCommand):
    """Command to list all users.

    Attributes:
        type: Command type identifier ("listUsers").
    """

    type: str = "listUsers"


@dataclass(kw_only=True)
class APISetActiveUser(BaseCommand):
    """Command to set the active user.

    Attributes:
        type: Command type identifier ("apiSetActiveUser").
        user_id: User identifier to set as active.
        view_pwd: Optional view password for encrypted data.
    """

    type: str = "apiSetActiveUser"
    user_id: int
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class APIHideUser(BaseCommand):
    """Command to hide a user profile.

    Attributes:
        type: Command type identifier ("apiHideUser").
        user_id: User identifier to hide.
        view_pwd: View password for encrypted data.
    """

    type: str = "apiHideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIUnhideUser(BaseCommand):
    """Command to unhide a user profile.

    Attributes:
        type: Command type identifier ("apiUnhideUser").
        user_id: User identifier to unhide.
        view_pwd: View password for encrypted data.
    """

    type: str = "apiUnhideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIMuteUser(BaseCommand):
    """Command to mute notifications for a user.

    Attributes:
        type: Command type identifier ("apiMuteUser").
        user_id: User identifier to mute.
    """

    type: str = "apiMuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIUnmuteUser(BaseCommand):
    """Command to unmute notifications for a user.

    Attributes:
        type: Command type identifier ("apiUnmuteUser").
        user_id: User identifier to unmute.
    """

    type: str = "apiUnmuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIDeleteUser(BaseCommand):
    """Command to delete a user profile.

    Attributes:
        type: Command type identifier ("apiDeleteUser").
        user_id: User identifier to delete.
        del_smp_queues: Whether to delete SMP queues.
        view_pwd: Optional view password for encrypted data.
    """

    type: str = "apiDeleteUser"
    user_id: int
    del_smp_queues: bool
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class APIUpdateProfile(BaseCommand):
    """Command to update a user profile.

    Attributes:
        type: Command type identifier ("apiUpdateProfile").
        user_id: User identifier to update.
        profile: New profile information.
    """

    type: str = "apiUpdateProfile"
    user_id: int
    profile: Profile
