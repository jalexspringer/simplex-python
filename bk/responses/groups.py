"""
Group-related response types for the Simplex messaging system.

This module defines response types for group-related operations, including:
- Group creation and profile management
- Group membership operations
- Group links and invitations
- Group member verification
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .base import CommandResponse


@dataclass
class GroupCreatedResponse(CommandResponse):
    """Response when a group is created."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupCreatedResponse":
        return cls(
            type="groupCreated",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class GroupMembersResponse(CommandResponse):
    """Response containing a list of group members."""

    group: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupMembersResponse":
        return cls(
            type="groupMembers", user=data.get("user"), group=data.get("group", {})
        )


@dataclass
class UserAcceptedGroupSentResponse(CommandResponse):
    """Response when the user has accepted a group and the acceptance is sent."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    hostContact: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserAcceptedGroupSentResponse":
        return cls(
            type="userAcceptedGroupSent",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            hostContact=data.get("hostContact"),
        )


@dataclass
class UserDeletedMemberResponse(CommandResponse):
    """Response when a user deletes a member from a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserDeletedMemberResponse":
        return cls(
            type="userDeletedMember",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class SentGroupInvitationResponse(CommandResponse):
    """Response when a group invitation is sent."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    contact: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SentGroupInvitationResponse":
        return cls(
            type="sentGroupInvitation",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            contact=data.get("contact", {}),
            member=data.get("member", {}),
        )


@dataclass
class LeftMemberUserResponse(CommandResponse):
    """Response when the user leaves a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LeftMemberUserResponse":
        return cls(
            type="leftMemberUser",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class GroupDeletedUserResponse(CommandResponse):
    """Response when a group is deleted for a user."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupDeletedUserResponse":
        return cls(
            type="groupDeletedUser",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class GroupUpdatedResponse(CommandResponse):
    """Response when a group profile is updated."""

    fromGroup: Dict[str, Any] = field(default_factory=dict)
    toGroup: Dict[str, Any] = field(default_factory=dict)
    member_: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupUpdatedResponse":
        return cls(
            type="groupUpdated",
            user=data.get("user"),
            fromGroup=data.get("fromGroup", {}),
            toGroup=data.get("toGroup", {}),
            member_=data.get("member_"),
        )


@dataclass
class GroupInvitationResponse(CommandResponse):
    """Response containing a group invitation."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupInvitationResponse":
        return cls(
            type="groupInvitation",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class ReceivedGroupInvitationResponse(CommandResponse):
    """Response when a group invitation is received."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    contact: Dict[str, Any] = field(default_factory=dict)
    memberRole: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReceivedGroupInvitationResponse":
        return cls(
            type="receivedGroupInvitation",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            contact=data.get("contact", {}),
            memberRole=data.get("memberRole", ""),
        )


@dataclass
class UserJoinedGroupResponse(CommandResponse):
    """Response when a user joins a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    hostMember: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserJoinedGroupResponse":
        return cls(
            type="userJoinedGroup",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            hostMember=data.get("hostMember", {}),
        )


@dataclass
class JoinedGroupMemberResponse(CommandResponse):
    """Response when a new member joins a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JoinedGroupMemberResponse":
        return cls(
            type="joinedGroupMember",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class JoinedGroupMemberConnectingResponse(CommandResponse):
    """Response when a joined group member is connecting."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    hostMember: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JoinedGroupMemberConnectingResponse":
        return cls(
            type="joinedGroupMemberConnecting",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            hostMember=data.get("hostMember", {}),
            member=data.get("member", {}),
        )


@dataclass
class ConnectedToGroupMemberResponse(CommandResponse):
    """Response when connected to a group member."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectedToGroupMemberResponse":
        return cls(
            type="connectedToGroupMember",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class DeletedMemberResponse(CommandResponse):
    """Response when a member is deleted from a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    byMember: Dict[str, Any] = field(default_factory=dict)
    deletedMember: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeletedMemberResponse":
        return cls(
            type="deletedMember",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            byMember=data.get("byMember", {}),
            deletedMember=data.get("deletedMember", {}),
        )


@dataclass
class DeletedMemberUserResponse(CommandResponse):
    """Response when a member is deleted for a user."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeletedMemberUserResponse":
        return cls(
            type="deletedMemberUser",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class LeftMemberResponse(CommandResponse):
    """Response when a member leaves a group."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LeftMemberResponse":
        return cls(
            type="leftMember",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class GroupRemovedResponse(CommandResponse):
    """Response when a group is removed."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupRemovedResponse":
        return cls(
            type="groupRemoved",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class GroupDeletedResponse(CommandResponse):
    """Response when a group is deleted."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupDeletedResponse":
        return cls(
            type="groupDeleted",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
        )


@dataclass
class GroupSubscribedResponse(CommandResponse):
    """Response when a group is subscribed to."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupSubscribedResponse":
        return cls(
            type="groupSubscribed",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class GroupEmptyResponse(CommandResponse):
    """Response when a group is empty."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupEmptyResponse":
        return cls(
            type="groupEmpty",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
        )


@dataclass
class MemberSubErrorResponse(CommandResponse):
    """Response when there's an error with a member subscription."""

    groupInfo: Dict[str, Any] = field(default_factory=dict)
    member: Dict[str, Any] = field(default_factory=dict)
    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemberSubErrorResponse":
        return cls(
            type="memberSubError",
            user=data.get("user"),
            groupInfo=data.get("groupInfo", {}),
            member=data.get("member", {}),
            chatError=data.get("chatError", {}),
        )


@dataclass
class MemberSubSummaryResponse(CommandResponse):
    """Response containing a summary of member subscriptions."""

    memberSubscriptions: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemberSubSummaryResponse":
        return cls(
            type="memberSubSummary",
            user=data.get("user"),
            memberSubscriptions=data.get("memberSubscriptions", []),
        )


# Supporting data classes that mirror those in the group.py commands file
@dataclass
class GroupProfile:
    """Group profile information."""

    displayName: str
    fullName: str
    image: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupProfile":
        return cls(
            displayName=data.get("displayName", ""),
            fullName=data.get("fullName", ""),
            image=data.get("image"),
        )


@dataclass
class GroupInfo:
    """Group information."""

    groupId: int
    localDisplayName: str
    groupProfile: GroupProfile
    membership: Dict[str, Any]
    createdAt: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupInfo":
        profile_data = data.get("groupProfile", {})
        group_profile = GroupProfile.from_dict(profile_data) if profile_data else None

        return cls(
            groupId=data.get("groupId", 0),
            localDisplayName=data.get("localDisplayName", ""),
            groupProfile=group_profile,
            membership=data.get("membership", {}),
            createdAt=data.get("createdAt", ""),
        )


@dataclass
class Group:
    """Group information with members."""

    groupInfo: GroupInfo
    members: List[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Group":
        group_info_data = data.get("groupInfo", {})
        group_info = GroupInfo.from_dict(group_info_data) if group_info_data else None

        return cls(groupInfo=group_info, members=data.get("members", []))
