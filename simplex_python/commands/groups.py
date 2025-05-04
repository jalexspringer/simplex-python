"""
Group management command classes for the Simplex messaging system.

This module defines the commands for managing groups, including:
- Group creation and configuration
- Member management (adding, removing, roles)
- Group links (creating, updating, deleting)
- Group information and verification

All commands inherit from BaseCommand and provide a consistent interface
for group-related operations in the Simplex system.
"""

from dataclasses import dataclass
from typing import Union, Optional
from .base import BaseCommand, GroupMemberRole

# Supporting data classes for group-related commands


@dataclass
class GroupProfile:
    """Group profile information."""

    displayName: str
    fullName: str  # can be empty string
    image: Optional[str] = None


@dataclass(kw_only=True)
class NewGroup(BaseCommand):
    """Command to create a new group."""

    type: str = "newGroup"
    groupProfile: GroupProfile


@dataclass(kw_only=True)
class APIAddMember(BaseCommand):
    """Command to add a member to a group via API."""

    type: str = "apiAddMember"
    groupId: int
    contactId: int
    memberRole: GroupMemberRole


@dataclass(kw_only=True)
class APIJoinGroup(BaseCommand):
    """Command to join a group via API."""

    type: str = "apiJoinGroup"
    groupId: int


@dataclass(kw_only=True)
class APIRemoveMember(BaseCommand):
    """Command to remove a member from a group via API."""

    type: str = "apiRemoveMember"
    groupId: int
    memberId: int


@dataclass(kw_only=True)
class APILeaveGroup(BaseCommand):
    """Command to leave a group via API."""

    type: str = "apiLeaveGroup"
    groupId: int


@dataclass(kw_only=True)
class APIListMembers(BaseCommand):
    """Command to list members of a group via API."""

    type: str = "apiListMembers"
    groupId: int


@dataclass(kw_only=True)
class APIUpdateGroupProfile(BaseCommand):
    """Command to update a group's profile via API."""

    type: str = "apiUpdateGroupProfile"
    groupId: int
    groupProfile: GroupProfile


@dataclass(kw_only=True)
class APICreateGroupLink(BaseCommand):
    """Command to create a group link via API."""

    type: str = "apiCreateGroupLink"
    groupId: int
    memberRole: GroupMemberRole


@dataclass(kw_only=True)
class APIGroupLinkMemberRole(BaseCommand):
    """Command to set the member role for a group link via API."""

    type: str = "apiGroupLinkMemberRole"
    groupId: int
    memberRole: GroupMemberRole


@dataclass(kw_only=True)
class APIDeleteGroupLink(BaseCommand):
    """Command to delete a group link via API."""

    type: str = "apiDeleteGroupLink"
    groupId: int


@dataclass(kw_only=True)
class APIGetGroupLink(BaseCommand):
    """Command to get a group link via API."""

    type: str = "apiGetGroupLink"
    groupId: int


@dataclass(kw_only=True)
class APIGroupMemberInfo(BaseCommand):
    """Command to get information about a group member via API."""

    type: str = "apiGroupMemberInfo"
    groupId: int
    memberId: int


@dataclass(kw_only=True)
class APIGetGroupMemberCode(BaseCommand):
    """Command to get a verification code for a group member via API."""

    type: str = "apiGetGroupMemberCode"
    groupId: int
    groupMemberId: int


@dataclass(kw_only=True)
class APIVerifyGroupMember(BaseCommand):
    """Command to verify a group member via API."""

    type: str = "apiVerifyGroupMember"
    groupId: int
    groupMemberId: int
    connectionCode: str


# Type alias for GroupCommand
GroupCommand = Union[
    NewGroup,
    APIAddMember,
    APIJoinGroup,
    APIRemoveMember,
    APILeaveGroup,
    APIListMembers,
    APIUpdateGroupProfile,
    APICreateGroupLink,
    APIGroupLinkMemberRole,
    APIDeleteGroupLink,
    APIGetGroupLink,
    APIGroupMemberInfo,
    APIGetGroupMemberCode,
    APIVerifyGroupMember,
]
