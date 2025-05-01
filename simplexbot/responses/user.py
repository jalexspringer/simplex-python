"""
User-related responses for Simplex messaging system.

This module defines response classes for user profile and contact management operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import BaseResponse, ChatResponseType
from ..models.chat import User, UserInfo, UserContactLink, Profile, ChatError


@dataclass(kw_only=True)
class CRActiveUser(BaseResponse):
    """Response for active user information.

    Attributes:
        type: Response type identifier ("activeUser").
        user: Active user information.
    """

    type: str = ChatResponseType.ACTIVE_USER.value
    user: User


@dataclass(kw_only=True)
class CRUsersList(BaseResponse):
    """Response for list of users.

    Attributes:
        type: Response type identifier ("usersList").
        users: List of user information with unread counts.
    """

    type: str = ChatResponseType.USERS_LIST.value
    users: List[UserInfo]


@dataclass(kw_only=True)
class CRUserProfile(BaseResponse):
    """Response for user profile information.

    Attributes:
        type: Response type identifier ("userProfile").
        user: User information.
        profile: User profile information.
    """

    type: str = ChatResponseType.USER_PROFILE.value
    user: User
    profile: Profile


@dataclass(kw_only=True)
class CRUserProfileNoChange(BaseResponse):
    """Response for no change in user profile.

    Attributes:
        type: Response type identifier ("userProfileNoChange").
        user: User information.
    """

    type: str = ChatResponseType.USER_PROFILE_NO_CHANGE.value
    user: User


@dataclass(kw_only=True)
class CRUserProfileUpdated(BaseResponse):
    """Response for updated user profile.

    Attributes:
        type: Response type identifier ("userProfileUpdated").
        user: User information.
        from_profile: Original profile information.
        to_profile: Updated profile information.
    """

    type: str = ChatResponseType.USER_PROFILE_UPDATED.value
    user: User
    from_profile: Profile
    to_profile: Profile


@dataclass(kw_only=True)
class CRUserContactLink(BaseResponse):
    """Response for user contact link information.

    Attributes:
        type: Response type identifier ("userContactLink").
        user: User information.
        contact_link: User contact link information.
    """

    type: str = ChatResponseType.USER_CONTACT_LINK.value
    user: User
    contact_link: UserContactLink


@dataclass(kw_only=True)
class CRUserContactLinkUpdated(BaseResponse):
    """Response for updated user contact link.

    Attributes:
        type: Response type identifier ("userContactLinkUpdated").
        user: User information.
        conn_req_contact: Connection request contact string.
        auto_accept: Whether to auto-accept connections.
        auto_reply: Optional auto-reply message content.
    """

    type: str = ChatResponseType.USER_CONTACT_LINK_UPDATED.value
    user: User
    conn_req_contact: str
    auto_accept: bool
    auto_reply: Optional[dict] = None


@dataclass(kw_only=True)
class CRUserContactLinkCreated(BaseResponse):
    """Response for created user contact link.

    Attributes:
        type: Response type identifier ("userContactLinkCreated").
        user: User information.
        conn_req_contact: Connection request contact string.
    """

    type: str = ChatResponseType.USER_CONTACT_LINK_CREATED.value
    user: User
    conn_req_contact: str


@dataclass(kw_only=True)
class CRUserContactLinkDeleted(BaseResponse):
    """Response for deleted user contact link.

    Attributes:
        type: Response type identifier ("userContactLinkDeleted").
        user: User information.
    """

    type: str = ChatResponseType.USER_CONTACT_LINK_DELETED.value
    user: User


@dataclass(kw_only=True)
class CRUserContactLinkSubscribed(BaseResponse):
    """Response for subscribed user contact link.

    Attributes:
        type: Response type identifier ("userContactLinkSubscribed").
    """

    type: str = ChatResponseType.USER_CONTACT_LINK_SUBSCRIBED.value


@dataclass(kw_only=True)
class CRUserContactLinkSubError(BaseResponse):
    """Response for user contact link subscription error.

    Attributes:
        type: Response type identifier ("userContactLinkSubError").
        chat_error: Chat error information.
    """

    type: str = ChatResponseType.USER_CONTACT_LINK_SUB_ERROR.value
    chat_error: ChatError


@dataclass(kw_only=True)
class CRUserProtoServers(BaseResponse):
    """Response for user protocol servers.

    Attributes:
        type: Response type identifier ("userProtoServers").
        user: User information.
        servers: Server configuration information.
    """

    type: str = ChatResponseType.USER_PROTO_SERVERS.value
    user: User
    servers: dict  # UserProtoServers
