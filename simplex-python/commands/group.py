"""
Group management commands for Simplex messaging system.

This module defines command classes for group-related operations:
- Creating and managing groups
- Group member operations
- Group invitation links
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseCommand, GroupMemberRole, GroupProfile


@dataclass(kw_only=True)
class NewGroup(BaseCommand):
    """Command to create a new group.

    Attributes:
        type: Command type identifier ("newGroup").
        group_profile: Group profile information.
    """

    type: str = "newGroup"
    group_profile: GroupProfile


@dataclass(kw_only=True)
class APIAddMember(BaseCommand):
    """Command to add a member to a group.

    Attributes:
        type: Command type identifier ("apiAddMember").
        group_id: Group identifier.
        contact_id: Contact identifier to add.
        member_role: Role to assign to the member.
    """

    type: str = "apiAddMember"
    group_id: int
    contact_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIJoinGroup(BaseCommand):
    """Command to join a group.

    Attributes:
        type: Command type identifier ("apiJoinGroup").
        group_id: Group identifier to join.
    """

    type: str = "apiJoinGroup"
    group_id: int


@dataclass(kw_only=True)
class APIRemoveMember(BaseCommand):
    """Command to remove a member from a group.

    Attributes:
        type: Command type identifier ("apiRemoveMember").
        group_id: Group identifier.
        member_id: Group member identifier to remove.
    """

    type: str = "apiRemoveMember"
    group_id: int
    member_id: int


@dataclass(kw_only=True)
class APILeaveGroup(BaseCommand):
    """Command to leave a group.

    Attributes:
        type: Command type identifier ("apiLeaveGroup").
        group_id: Group identifier to leave.
    """

    type: str = "apiLeaveGroup"
    group_id: int


@dataclass(kw_only=True)
class APIListMembers(BaseCommand):
    """Command to list members of a group.

    Attributes:
        type: Command type identifier ("apiListMembers").
        group_id: Group identifier.
    """

    type: str = "apiListMembers"
    group_id: int


@dataclass(kw_only=True)
class APIUpdateGroupProfile(BaseCommand):
    """Command to update a group's profile.

    Attributes:
        type: Command type identifier ("apiUpdateGroupProfile").
        group_id: Group identifier.
        group_profile: New group profile information.
    """

    type: str = "apiUpdateGroupProfile"
    group_id: int
    group_profile: GroupProfile


@dataclass(kw_only=True)
class APICreateGroupLink(BaseCommand):
    """Command to create a group invitation link.

    Attributes:
        type: Command type identifier ("apiCreateGroupLink").
        group_id: Group identifier.
        member_role: Role for members who join via the link.
    """

    type: str = "apiCreateGroupLink"
    group_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIGroupLinkMemberRole(BaseCommand):
    """Command to update the role for members who join via a group link.

    Attributes:
        type: Command type identifier ("apiGroupLinkMemberRole").
        group_id: Group identifier.
        member_role: New role for members who join via the link.
    """

    type: str = "apiGroupLinkMemberRole"
    group_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIDeleteGroupLink(BaseCommand):
    """Command to delete a group invitation link.

    Attributes:
        type: Command type identifier ("apiDeleteGroupLink").
        group_id: Group identifier.
    """

    type: str = "apiDeleteGroupLink"
    group_id: int


@dataclass(kw_only=True)
class APIGetGroupLink(BaseCommand):
    """Command to get a group's invitation link.

    Attributes:
        type: Command type identifier ("apiGetGroupLink").
        group_id: Group identifier.
    """

    type: str = "apiGetGroupLink"
    group_id: int


@dataclass(kw_only=True)
class APIGroupMemberInfo(BaseCommand):
    """Command to get information about a group member.

    Attributes:
        type: Command type identifier ("apiGroupMemberInfo").
        group_id: Group identifier.
        member_id: Group member identifier.
    """

    type: str = "apiGroupMemberInfo"
    group_id: int
    member_id: int


@dataclass(kw_only=True)
class APIGetGroupMemberCode(BaseCommand):
    """Command to get a verification code for a group member.

    Attributes:
        type: Command type identifier ("apiGetGroupMemberCode").
        group_id: Group identifier.
        group_member_id: Group member identifier.
    """

    type: str = "apiGetGroupMemberCode"
    group_id: int
    group_member_id: int


@dataclass(kw_only=True)
class APIVerifyGroupMember(BaseCommand):
    """Command to verify a group member using a connection code.

    Attributes:
        type: Command type identifier ("apiVerifyGroupMember").
        group_id: Group identifier.
        group_member_id: Group member identifier.
        connection_code: Connection verification code.
    """

    type: str = "apiVerifyGroupMember"
    group_id: int
    group_member_id: int
    connection_code: Optional[str] = None
