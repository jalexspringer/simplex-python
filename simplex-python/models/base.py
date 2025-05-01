"""
Base models for Simplex data structures.

This module contains base data model classes used across the Simplex messaging system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


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
