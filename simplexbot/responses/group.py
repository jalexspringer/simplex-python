"""
Group-related responses for Simplex messaging system.

This module defines response classes for group operations and member management.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import BaseResponse, ChatResponseType
from ..models.chat import (
    User,
    Group,
    GroupInfo,
    GroupMember,
    ContactSubStatus,
    Contact,
    ChatError,
    ConnectionStats,
)
from ..commands.base import GroupMemberRole


@dataclass(kw_only=True)
class CRGroupMemberInfo(BaseResponse):
    """Response for group member information.

    Attributes:
        type: Response type identifier ("groupMemberInfo").
        user: User information.
        group_info: Group information.
        member: Group member information.
        connection_stats_: Optional connection statistics.
    """

    type: str = ChatResponseType.GROUP_MEMBER_INFO.value
    user: User
    group_info: GroupInfo
    member: GroupMember
    connection_stats_: Optional[ConnectionStats] = None


@dataclass(kw_only=True)
class CRGroupEmpty(BaseResponse):
    """Response for empty group.

    Attributes:
        type: Response type identifier ("groupEmpty").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_EMPTY.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRMemberSubError(BaseResponse):
    """Response for member subscription error.

    Attributes:
        type: Response type identifier ("memberSubError").
        user: User information.
        group_info: Group information.
        member: Group member information.
        chat_error: Chat error information.
    """

    type: str = ChatResponseType.MEMBER_SUB_ERROR.value
    user: User
    group_info: GroupInfo
    member: GroupMember
    chat_error: ChatError


@dataclass(kw_only=True)
class CRMemberSubSummary(BaseResponse):
    """Response for member subscription summary.

    Attributes:
        type: Response type identifier ("memberSubSummary").
        user: User information.
        member_subscriptions: List of member subscription status.
    """

    type: str = ChatResponseType.MEMBER_SUB_SUMMARY.value
    user: User
    member_subscriptions: List[ContactSubStatus]


@dataclass(kw_only=True)
class CRGroupSubscribed(BaseResponse):
    """Response for subscribed group.

    Attributes:
        type: Response type identifier ("groupSubscribed").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_SUBSCRIBED.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRGroupCreated(BaseResponse):
    """Response for created group.

    Attributes:
        type: Response type identifier ("groupCreated").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_CREATED.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRGroupMembers(BaseResponse):
    """Response for group members.

    Attributes:
        type: Response type identifier ("groupMembers").
        user: User information.
        group: Group information with members.
    """

    type: str = ChatResponseType.GROUP_MEMBERS.value
    user: User
    group: Group


@dataclass(kw_only=True)
class CRUserAcceptedGroupSent(BaseResponse):
    """Response for user accepted group invitation.

    Attributes:
        type: Response type identifier ("userAcceptedGroupSent").
        user: User information.
        group_info: Group information.
        host_contact: Optional host contact information (for group links).
    """

    type: str = ChatResponseType.USER_ACCEPTED_GROUP_SENT.value
    user: User
    group_info: GroupInfo
    host_contact: Optional[Contact] = None


@dataclass(kw_only=True)
class CRUserDeletedMember(BaseResponse):
    """Response for user deleted a member.

    Attributes:
        type: Response type identifier ("userDeletedMember").
        user: User information.
        group_info: Group information.
        member: Group member information.
    """

    type: str = ChatResponseType.USER_DELETED_MEMBER.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRSentGroupInvitation(BaseResponse):
    """Response for sent group invitation.

    Attributes:
        type: Response type identifier ("sentGroupInvitation").
        user: User information.
        group_info: Group information.
        contact: Contact information.
        member: Group member information.
    """

    type: str = ChatResponseType.SENT_GROUP_INVITATION.value
    user: User
    group_info: GroupInfo
    contact: Contact
    member: GroupMember


@dataclass(kw_only=True)
class CRLeftMemberUser(BaseResponse):
    """Response for user left the group.

    Attributes:
        type: Response type identifier ("leftMemberUser").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.LEFT_MEMBER_USER.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRGroupDeletedUser(BaseResponse):
    """Response for user was deleted from the group.

    Attributes:
        type: Response type identifier ("groupDeletedUser").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_DELETED_USER.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRGroupInvitation(BaseResponse):
    """Response for group invitation.

    Attributes:
        type: Response type identifier ("groupInvitation").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_INVITATION.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRReceivedGroupInvitation(BaseResponse):
    """Response for received group invitation.

    Attributes:
        type: Response type identifier ("receivedGroupInvitation").
        user: User information.
        group_info: Group information.
        contact: Contact information.
        member_role: Group member role.
    """

    type: str = ChatResponseType.RECEIVED_GROUP_INVITATION.value
    user: User
    group_info: GroupInfo
    contact: Contact
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class CRUserJoinedGroup(BaseResponse):
    """Response for user joined a group.

    Attributes:
        type: Response type identifier ("userJoinedGroup").
        user: User information.
        group_info: Group information.
        host_member: Host member information.
    """

    type: str = ChatResponseType.USER_JOINED_GROUP.value
    user: User
    group_info: GroupInfo
    host_member: GroupMember


@dataclass(kw_only=True)
class CRJoinedGroupMember(BaseResponse):
    """Response for a member joined the group.

    Attributes:
        type: Response type identifier ("joinedGroupMember").
        user: User information.
        group_info: Group information.
        member: Group member information.
    """

    type: str = ChatResponseType.JOINED_GROUP_MEMBER.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRJoinedGroupMemberConnecting(BaseResponse):
    """Response for connecting to a joined group member.

    Attributes:
        type: Response type identifier ("joinedGroupMemberConnecting").
        user: User information.
        group_info: Group information.
        host_member: Host member information.
        member: Group member information.
    """

    type: str = ChatResponseType.JOINED_GROUP_MEMBER_CONNECTING.value
    user: User
    group_info: GroupInfo
    host_member: GroupMember
    member: GroupMember


@dataclass(kw_only=True)
class CRConnectedToGroupMember(BaseResponse):
    """Response for connected to a group member.

    Attributes:
        type: Response type identifier ("connectedToGroupMember").
        user: User information.
        group_info: Group information.
        member: Group member information.
    """

    type: str = ChatResponseType.CONNECTED_TO_GROUP_MEMBER.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRDeletedMember(BaseResponse):
    """Response for deleted group member.

    Attributes:
        type: Response type identifier ("deletedMember").
        user: User information.
        group_info: Group information.
        by_member: Member who performed the deletion.
        deleted_member: Deleted member information.
    """

    type: str = ChatResponseType.DELETED_MEMBER.value
    user: User
    group_info: GroupInfo
    by_member: GroupMember
    deleted_member: GroupMember


@dataclass(kw_only=True)
class CRDeletedMemberUser(BaseResponse):
    """Response for user was deleted as a member.

    Attributes:
        type: Response type identifier ("deletedMemberUser").
        user: User information.
        group_info: Group information.
        member: Member who performed the deletion.
    """

    type: str = ChatResponseType.DELETED_MEMBER_USER.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRLeftMember(BaseResponse):
    """Response for a member left the group.

    Attributes:
        type: Response type identifier ("leftMember").
        user: User information.
        group_info: Group information.
        member: Group member information.
    """

    type: str = ChatResponseType.LEFT_MEMBER.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRGroupRemoved(BaseResponse):
    """Response for removed group.

    Attributes:
        type: Response type identifier ("groupRemoved").
        user: User information.
        group_info: Group information.
    """

    type: str = ChatResponseType.GROUP_REMOVED.value
    user: User
    group_info: GroupInfo


@dataclass(kw_only=True)
class CRGroupDeleted(BaseResponse):
    """Response for deleted group.

    Attributes:
        type: Response type identifier ("groupDeleted").
        user: User information.
        group_info: Group information.
        member: Group member information.
    """

    type: str = ChatResponseType.GROUP_DELETED.value
    user: User
    group_info: GroupInfo
    member: GroupMember


@dataclass(kw_only=True)
class CRGroupUpdated(BaseResponse):
    """Response for updated group.

    Attributes:
        type: Response type identifier ("groupUpdated").
        user: User information.
        from_group: Original group information.
        to_group: Updated group information.
        member_: Optional member who performed the update.
    """

    type: str = ChatResponseType.GROUP_UPDATED.value
    user: User
    from_group: GroupInfo
    to_group: GroupInfo
    member_: Optional[GroupMember] = None
