"""
Base response types for Simplex messaging system.

This module defines the base response class from which all response types inherit.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable


class ChatResponseType(Enum):
    """Enumeration of response types.

    This enum lists all possible response type identifiers.
    """

    ACTIVE_USER = "activeUser"
    USERS_LIST = "usersList"
    CHAT_STARTED = "chatStarted"
    CHAT_RUNNING = "chatRunning"
    CHAT_STOPPED = "chatStopped"
    API_CHATS = "apiChats"
    API_CHAT = "apiChat"
    API_PARSED_MARKDOWN = "apiParsedMarkdown"
    USER_PROTO_SERVERS = "userProtoServers"
    CONTACT_INFO = "contactInfo"
    GROUP_MEMBER_INFO = "groupMemberInfo"
    NEW_CHAT_ITEMS = "newChatItems"
    CHAT_ITEM_STATUS_UPDATED = "chatItemStatusUpdated"
    CHAT_ITEM_UPDATED = "chatItemUpdated"
    CHAT_ITEM_DELETED = "chatItemDeleted"
    MSG_INTEGRITY_ERROR = "msgIntegrityError"
    CMD_OK = "cmdOk"
    USER_CONTACT_LINK = "userContactLink"
    USER_CONTACT_LINK_UPDATED = "userContactLinkUpdated"
    USER_CONTACT_LINK_CREATED = "userContactLinkCreated"
    USER_CONTACT_LINK_DELETED = "userContactLinkDeleted"
    CONTACT_REQUEST_REJECTED = "contactRequestRejected"
    USER_PROFILE = "userProfile"
    USER_PROFILE_NO_CHANGE = "userProfileNoChange"
    USER_PROFILE_UPDATED = "userProfileUpdated"
    CONTACT_ALIAS_UPDATED = "contactAliasUpdated"
    INVITATION = "invitation"
    SENT_CONFIRMATION = "sentConfirmation"
    SENT_INVITATION = "sentInvitation"
    CONTACT_UPDATED = "contactUpdated"
    CONTACTS_MERGED = "contactsMerged"
    CONTACT_DELETED = "contactDeleted"
    CHAT_CLEARED = "chatCleared"
    RECEIVED_CONTACT_REQUEST = "receivedContactRequest"
    ACCEPTING_CONTACT_REQUEST = "acceptingContactRequest"
    CONTACT_ALREADY_EXISTS = "contactAlreadyExists"
    CONTACT_REQUEST_ALREADY_ACCEPTED = "contactRequestAlreadyAccepted"
    CONTACT_CONNECTING = "contactConnecting"
    CONTACT_CONNECTED = "contactConnected"
    CONTACT_ANOTHER_CLIENT = "contactAnotherClient"
    CONTACT_SUB_ERROR = "contactSubError"
    CONTACT_SUB_SUMMARY = "contactSubSummary"
    CONTACTS_DISCONNECTED = "contactsDisconnected"
    CONTACTS_SUBSCRIBED = "contactsSubscribed"
    HOST_CONNECTED = "hostConnected"
    HOST_DISCONNECTED = "hostDisconnected"
    GROUP_EMPTY = "groupEmpty"
    MEMBER_SUB_ERROR = "memberSubError"
    MEMBER_SUB_SUMMARY = "memberSubSummary"
    GROUP_SUBSCRIBED = "groupSubscribed"
    RCV_FILE_ACCEPTED = "rcvFileAccepted"
    RCV_FILE_ACCEPTED_SND_CANCELLED = "rcvFileAcceptedSndCancelled"
    RCV_FILE_START = "rcvFileStart"
    RCV_FILE_COMPLETE = "rcvFileComplete"
    RCV_FILE_CANCELLED = "rcvFileCancelled"
    RCV_FILE_SND_CANCELLED = "rcvFileSndCancelled"
    SND_FILE_START = "sndFileStart"
    SND_FILE_COMPLETE = "sndFileComplete"
    SND_FILE_CANCELLED = "sndFileCancelled"
    SND_FILE_RCV_CANCELLED = "sndFileRcvCancelled"
    SND_GROUP_FILE_CANCELLED = "sndGroupFileCancelled"
    SND_FILE_SUB_ERROR = "sndFileSubError"
    RCV_FILE_SUB_ERROR = "rcvFileSubError"
    PENDING_SUB_SUMMARY = "pendingSubSummary"
    GROUP_CREATED = "groupCreated"
    GROUP_MEMBERS = "groupMembers"
    USER_ACCEPTED_GROUP_SENT = "userAcceptedGroupSent"
    USER_DELETED_MEMBER = "userDeletedMember"
    SENT_GROUP_INVITATION = "sentGroupInvitation"
    LEFT_MEMBER_USER = "leftMemberUser"
    GROUP_DELETED_USER = "groupDeletedUser"
    GROUP_INVITATION = "groupInvitation"
    RECEIVED_GROUP_INVITATION = "receivedGroupInvitation"
    USER_JOINED_GROUP = "userJoinedGroup"
    JOINED_GROUP_MEMBER = "joinedGroupMember"
    JOINED_GROUP_MEMBER_CONNECTING = "joinedGroupMemberConnecting"
    CONNECTED_TO_GROUP_MEMBER = "connectedToGroupMember"
    DELETED_MEMBER = "deletedMember"
    DELETED_MEMBER_USER = "deletedMemberUser"
    LEFT_MEMBER = "leftMember"
    GROUP_REMOVED = "groupRemoved"
    GROUP_DELETED = "groupDeleted"
    GROUP_UPDATED = "groupUpdated"
    USER_CONTACT_LINK_SUBSCRIBED = "userContactLinkSubscribed"
    USER_CONTACT_LINK_SUB_ERROR = "userContactLinkSubError"
    CONTACT_CONNECTION_DELETED = "contactConnectionDeleted"
    MESSAGE_ERROR = "messageError"
    CHAT_CMD_ERROR = "chatCmdError"
    CHAT_ERROR = "chatError"


@runtime_checkable
class Response(Protocol):
    """Protocol defining the basic interface of all response objects.

    All response classes should have a type property that identifies the response.
    """

    type: str


@dataclass(kw_only=True)
class BaseResponse(ABC):
    """Abstract base class for all response objects.

    This class provides common functionality for all responses and ensures
    they conform to the Response protocol.

    Attributes:
        type: String identifier for the response type.
    """

    type: str
