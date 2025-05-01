"""
Chat models for Simplex messaging system.

This module defines structures for chat information, items, and related data.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Any, Dict, Union

from .base import Profile, LocalProfile, GroupProfile
from .message import MsgContent


class ChatInfoType(Enum):
    """Enumeration of chat info types.

    Attributes:
        DIRECT: Direct (one-to-one) chat.
        GROUP: Group chat.
        CONTACT_REQUEST: Contact request chat.
    """

    DIRECT = "direct"
    GROUP = "group"
    CONTACT_REQUEST = "contactRequest"


@dataclass(kw_only=True)
class Contact:
    """Information about a contact.

    Attributes:
        contact_id: Contact identifier.
        local_display_name: Local display name.
        profile: Contact profile information.
        active_conn: Active connection information.
        via_group: Optional group identifier through which contact was added.
        created_at: Creation timestamp.
    """

    contact_id: int
    local_display_name: str
    profile: Profile
    active_conn: Connection
    via_group: Optional[int] = None
    created_at: datetime


@dataclass(kw_only=True)
class ContactRef:
    """Reference to a contact.

    Attributes:
        contact_id: Contact identifier.
        local_display_name: Local display name.
    """

    contact_id: int
    local_display_name: str


@dataclass(kw_only=True)
class GroupMember:
    """Group member information.

    Attributes:
        group_member_id: Group member identifier.
        member_id: Member identifier string.
        member_role: Role in the group.
        local_display_name: Local display name.
        member_profile: Member profile information.
        member_contact_id: Optional contact identifier.
        active_conn: Optional active connection information.
    """

    group_member_id: int
    member_id: str
    member_role: str  # GroupMemberRole as string
    local_display_name: str
    member_profile: Profile
    member_contact_id: Optional[int] = None
    active_conn: Optional[Connection] = None


@dataclass(kw_only=True)
class GroupInfo:
    """Information about a group.

    Attributes:
        group_id: Group identifier.
        local_display_name: Local display name.
        group_profile: Group profile information.
        membership: Current user's membership in group.
        created_at: Creation timestamp.
    """

    group_id: int
    local_display_name: str
    group_profile: GroupProfile
    membership: GroupMember
    created_at: datetime


@dataclass(kw_only=True)
class Group:
    """A group with its members.

    Attributes:
        group_info: Group information.
        members: List of group members.
    """

    group_info: GroupInfo
    members: List[GroupMember]


@dataclass(kw_only=True)
class UserContactRequest:
    """Contact request information.

    Attributes:
        contact_request_id: Contact request identifier.
        local_display_name: Local display name.
        profile: Profile information.
        created_at: Creation timestamp.
    """

    contact_request_id: int
    local_display_name: str
    profile: Profile
    created_at: datetime


@dataclass(kw_only=True)
class Connection:
    """Connection information.

    Attributes:
        conn_id: Connection identifier.
    """

    conn_id: int


@dataclass(kw_only=True)
class User:
    """User information.

    Attributes:
        user_id: User identifier.
        agent_user_id: Agent user identifier.
        user_contact_id: User contact identifier.
        local_display_name: Local display name.
        profile: User profile information.
        active_user: Whether this is the active user.
        view_pwd_hash: Password hash for viewing.
        show_ntfs: Whether to show notifications.
    """

    user_id: int
    agent_user_id: str
    user_contact_id: int
    local_display_name: str
    profile: LocalProfile
    active_user: bool
    view_pwd_hash: str
    show_ntfs: bool


@dataclass(kw_only=True)
class UserInfo:
    """User information with unread count.

    Attributes:
        user: User information.
        unread_count: Number of unread messages.
    """

    user: User
    unread_count: int


@dataclass(kw_only=True)
class ChatStats:
    """Statistics for a chat.

    Attributes:
        unread_count: Number of unread messages.
        min_unread_item_id: Minimum unread item identifier.
    """

    unread_count: int
    min_unread_item_id: int


class ChatDirectionType(Enum):
    """Enumeration of chat direction types.

    Attributes:
        DIRECT_SND: Direct send.
        DIRECT_RCV: Direct receive.
        GROUP_SND: Group send.
        GROUP_RCV: Group receive.
    """

    DIRECT_SND = "directSnd"
    DIRECT_RCV = "directRcv"
    GROUP_SND = "groupSnd"
    GROUP_RCV = "groupRcv"


@dataclass(kw_only=True)
class CIDirectSnd:
    """Direct send chat direction.

    Attributes:
        type: Direction type ("directSnd").
    """

    type: str = ChatDirectionType.DIRECT_SND.value


@dataclass(kw_only=True)
class CIDirectRcv:
    """Direct receive chat direction.

    Attributes:
        type: Direction type ("directRcv").
    """

    type: str = ChatDirectionType.DIRECT_RCV.value


@dataclass(kw_only=True)
class CIGroupSnd:
    """Group send chat direction.

    Attributes:
        type: Direction type ("groupSnd").
    """

    type: str = ChatDirectionType.GROUP_SND.value


@dataclass(kw_only=True)
class CIGroupRcv:
    """Group receive chat direction.

    Attributes:
        type: Direction type ("groupRcv").
        group_member: Group member information.
    """

    type: str = ChatDirectionType.GROUP_RCV.value
    group_member: GroupMember


# Chat direction union type
CIDirection = Union[CIDirectSnd, CIDirectRcv, CIGroupSnd, CIGroupRcv]


class ChatStatusType(Enum):
    """Enumeration of chat status types.

    Attributes:
        SND_NEW: Newly sent.
        SND_SENT: Successfully sent.
        SND_ERROR_AUTH: Authentication error when sending.
        SND_ERROR: General error when sending.
        RCV_NEW: Newly received.
        RCV_READ: Received and read.
    """

    SND_NEW = "sndNew"
    SND_SENT = "sndSent"
    SND_ERROR_AUTH = "sndErrorAuth"
    SND_ERROR = "sndError"
    RCV_NEW = "rcvNew"
    RCV_READ = "rcvRead"


@dataclass(kw_only=True)
class CISndNew:
    """New sent status.

    Attributes:
        type: Status type ("sndNew").
    """

    type: str = ChatStatusType.SND_NEW.value


@dataclass(kw_only=True)
class CISndSent:
    """Sent status.

    Attributes:
        type: Status type ("sndSent").
    """

    type: str = ChatStatusType.SND_SENT.value


@dataclass(kw_only=True)
class CISndErrorAuth:
    """Authentication error status.

    Attributes:
        type: Status type ("sndErrorAuth").
    """

    type: str = ChatStatusType.SND_ERROR_AUTH.value


@dataclass(kw_only=True)
class CISndError:
    """Send error status.

    Attributes:
        type: Status type ("sndError").
        agent_error: Agent error information.
    """

    type: str = ChatStatusType.SND_ERROR.value
    agent_error: AgentErrorType


@dataclass(kw_only=True)
class CIRcvNew:
    """New received status.

    Attributes:
        type: Status type ("rcvNew").
    """

    type: str = ChatStatusType.RCV_NEW.value


@dataclass(kw_only=True)
class CIRcvRead:
    """Read received status.

    Attributes:
        type: Status type ("rcvRead").
    """

    type: str = ChatStatusType.RCV_READ.value


# Chat status union type
CIStatus = Union[CISndNew, CISndSent, CISndErrorAuth, CISndError, CIRcvNew, CIRcvRead]


@dataclass(kw_only=True)
class CIMeta:
    """Chat item metadata.

    Attributes:
        item_id: Item identifier.
        item_ts: Item timestamp.
        item_text: Item text.
        item_status: Item status.
        created_at: Creation timestamp.
        item_deleted: Whether item is deleted.
        item_edited: Whether item is edited.
        editable: Whether item is editable.
    """

    item_id: int
    item_ts: datetime
    item_text: str
    item_status: CIStatus
    created_at: datetime
    item_deleted: bool
    item_edited: bool
    editable: bool


@dataclass(kw_only=True)
class FormattedText:
    """Formatted text information.

    This class serves as a placeholder for formatted text structures.
    """

    pass


@dataclass(kw_only=True)
class CIQuote:
    """Quote information for a chat item.

    Attributes:
        chat_dir: Optional direction of original message.
        item_id: Optional item identifier of original message.
        shared_msg_id: Optional shared message identifier.
        sent_at: When the original message was sent.
        content: Content of the original message.
        formatted_text: Optional formatted text.
    """

    sent_at: datetime
    content: MsgContent
    chat_dir: Optional[CIDirection] = None
    item_id: Optional[int] = None
    shared_msg_id: Optional[str] = None
    formatted_text: Optional[List[FormattedText]] = None


class ChatContentType(Enum):
    """Enumeration of chat content types.

    Attributes:
        SND_MSG_CONTENT: Sent message content.
        RCV_MSG_CONTENT: Received message content.
        SND_DELETED: Sent deleted message.
        RCV_DELETED: Received deleted message.
        SND_FILE_INVITATION: Sent file invitation.
        RCV_FILE_INVITATION: Received file invitation.
    """

    SND_MSG_CONTENT = "sndMsgContent"
    RCV_MSG_CONTENT = "rcvMsgContent"
    SND_DELETED = "sndDeleted"
    RCV_DELETED = "rcvDeleted"
    SND_FILE_INVITATION = "sndFileInvitation"
    RCV_FILE_INVITATION = "rcvFileInvitation"


@dataclass(kw_only=True)
class CISndMsgContent:
    """Sent message content.

    Attributes:
        type: Content type ("sndMsgContent").
        msg_content: Message content.
    """

    type: str = ChatContentType.SND_MSG_CONTENT.value
    msg_content: MsgContent


@dataclass(kw_only=True)
class CIRcvMsgContent:
    """Received message content.

    Attributes:
        type: Content type ("rcvMsgContent").
        msg_content: Message content.
    """

    type: str = ChatContentType.RCV_MSG_CONTENT.value
    msg_content: MsgContent


@dataclass(kw_only=True)
class CISndDeleted:
    """Sent deleted content.

    Attributes:
        type: Content type ("sndDeleted").
        delete_mode: Deletion mode.
    """

    type: str = ChatContentType.SND_DELETED.value
    delete_mode: str  # DeleteMode as string


@dataclass(kw_only=True)
class CIRcvDeleted:
    """Received deleted content.

    Attributes:
        type: Content type ("rcvDeleted").
        delete_mode: Deletion mode.
    """

    type: str = ChatContentType.RCV_DELETED.value
    delete_mode: str  # DeleteMode as string


@dataclass(kw_only=True)
class CISndFileInvitation:
    """Sent file invitation.

    Attributes:
        type: Content type ("sndFileInvitation").
        file_id: File identifier.
        file_path: File path.
    """

    type: str = ChatContentType.SND_FILE_INVITATION.value
    file_id: int
    file_path: str


@dataclass(kw_only=True)
class CIRcvFileInvitation:
    """Received file invitation.

    Attributes:
        type: Content type ("rcvFileInvitation").
        rcv_file_transfer: Received file transfer information.
    """

    type: str = ChatContentType.RCV_FILE_INVITATION.value
    rcv_file_transfer: RcvFileTransfer


# Chat content union type
CIContent = Union[
    CISndMsgContent,
    CIRcvMsgContent,
    CISndDeleted,
    CIRcvDeleted,
    CISndFileInvitation,
    CIRcvFileInvitation,
]


@dataclass(kw_only=True)
class ChatItem:
    """Chat item information.

    Attributes:
        chat_dir: Direction of the chat item.
        meta: Metadata for the chat item.
        content: Content of the chat item.
        formatted_text: Optional formatted text.
        quoted_item: Optional quoted item.
    """

    chat_dir: CIDirection
    meta: CIMeta
    content: CIContent
    formatted_text: Optional[List[FormattedText]] = None
    quoted_item: Optional[CIQuote] = None


@dataclass(kw_only=True)
class CInfoDirect:
    """Direct chat information.

    Attributes:
        type: Chat info type ("direct").
        contact: Contact information.
    """

    type: str = ChatInfoType.DIRECT.value
    contact: Contact


@dataclass(kw_only=True)
class CInfoGroup:
    """Group chat information.

    Attributes:
        type: Chat info type ("group").
        group_info: Group information.
    """

    type: str = ChatInfoType.GROUP.value
    group_info: GroupInfo


@dataclass(kw_only=True)
class CInfoContactRequest:
    """Contact request chat information.

    Attributes:
        type: Chat info type ("contactRequest").
        contact_request: Contact request information.
    """

    type: str = ChatInfoType.CONTACT_REQUEST.value
    contact_request: UserContactRequest


# Chat info union type
ChatInfo = Union[CInfoDirect, CInfoGroup, CInfoContactRequest]


@dataclass(kw_only=True)
class AChatItem:
    """Chat item with context information.

    Attributes:
        chat_info: Chat information.
        chat_item: Chat item.
    """

    chat_info: ChatInfo
    chat_item: ChatItem


@dataclass(kw_only=True)
class Chat:
    """Chat with items and statistics.

    Attributes:
        chat_info: Chat information.
        chat_items: Chat items.
        chat_stats: Chat statistics.
    """

    chat_info: ChatInfo
    chat_items: List[ChatItem]
    chat_stats: ChatStats


@dataclass(kw_only=True)
class RcvFileTransfer:
    """Information about a received file transfer.

    Attributes:
        file_id: File identifier.
        sender_display_name: Sender's display name.
        chunk_size: Size of each chunk.
        cancelled: Whether transfer was cancelled.
        grp_member_id: Optional group member identifier.
    """

    file_id: int
    sender_display_name: str
    chunk_size: int
    cancelled: bool
    grp_member_id: Optional[int] = None


@dataclass(kw_only=True)
class SndFileTransfer:
    """Information about a sent file transfer.

    Attributes:
        file_id: File identifier.
        file_name: File name.
        file_path: File path.
        file_size: File size.
        chunk_size: Size of each chunk.
        recipient_display_name: Recipient's display name.
        conn_id: Connection identifier.
    """

    file_id: int
    file_name: str
    file_path: str
    file_size: int
    chunk_size: int
    recipient_display_name: str
    conn_id: int


@dataclass(kw_only=True)
class FileTransferMeta:
    """Metadata for a file transfer.

    Attributes:
        file_id: File identifier.
        file_name: File name.
        file_path: File path.
        file_size: File size.
        chunk_size: Size of each chunk.
        cancelled: Whether transfer was cancelled.
    """

    file_id: int
    file_name: str
    file_path: str
    file_size: int
    chunk_size: int
    cancelled: bool


@dataclass(kw_only=True)
class UserContactLink:
    """User contact link information.

    Attributes:
        conn_req_contact: Connection request contact.
        auto_accept: Optional auto-accept configuration.
    """

    conn_req_contact: str
    auto_accept: Optional[AutoAccept] = None


@dataclass(kw_only=True)
class AutoAccept:
    """Auto-accept configuration.

    Attributes:
        accept_incognito: Whether to accept incognito connections.
        auto_reply: Optional automatic reply message.
    """

    accept_incognito: bool
    auto_reply: Optional[MsgContent] = None


@dataclass(kw_only=True)
class AgentErrorType:
    """Agent error information.

    Attributes:
        type: Error type.
        additional_fields: Additional error fields.
    """

    type: str
    additional_fields: Dict[str, Any] = None


@dataclass(kw_only=True)
class StoreErrorType:
    """Store error information.

    Attributes:
        type: Error type.
        additional_fields: Additional error fields.
    """

    type: str
    additional_fields: Dict[str, Any] = None


@dataclass(kw_only=True)
class ConnectionStats:
    """Connection statistics.

    Attributes:
        rcv_servers: Optional list of receive servers.
        snd_servers: Optional list of send servers.
    """

    rcv_servers: Optional[List[str]] = None
    snd_servers: Optional[List[str]] = None


@dataclass(kw_only=True)
class PendingContactConnection:
    """Pending contact connection information.

    This class serves as a placeholder for pending contact connection structures.
    """

    pass


@dataclass(kw_only=True)
class ContactSubStatus:
    """Contact subscription status.

    This class serves as a placeholder for contact subscription status structures.
    """

    pass


@dataclass(kw_only=True)
class MemberSubStatus:
    """Member subscription status.

    Attributes:
        member: Group member information.
        member_error: Optional chat error.
    """

    member: GroupMember
    member_error: Optional[ChatError] = None


@dataclass(kw_only=True)
class PendingSubStatus:
    """Pending subscription status.

    This class serves as a placeholder for pending subscription status structures.
    """

    pass


@dataclass(kw_only=True)
class MsgErrorType:
    """Message error information.

    This class serves as a placeholder for message error type structures.
    """

    pass


class ChatErrorType(Enum):
    """Enumeration of chat error types.

    Attributes:
        NO_ACTIVE_USER: No active user.
        ACTIVE_USER_EXISTS: Active user already exists.
    """

    NO_ACTIVE_USER = "noActiveUser"
    ACTIVE_USER_EXISTS = "activeUserExists"


@dataclass(kw_only=True)
class CENoActiveUser:
    """No active user error.

    Attributes:
        type: Error type ("noActiveUser").
    """

    type: str = ChatErrorType.NO_ACTIVE_USER.value


@dataclass(kw_only=True)
class CEActiveUserExists:
    """Active user exists error.

    Attributes:
        type: Error type ("activeUserExists").
    """

    type: str = ChatErrorType.ACTIVE_USER_EXISTS.value


# Chat error type union
ChatErrorType = Union[CENoActiveUser, CEActiveUserExists]


@dataclass(kw_only=True)
class ChatErrorChat:
    """Chat error.

    Attributes:
        type: Error type ("error").
        error_type: Specific error type.
    """

    type: str = "error"
    error_type: ChatErrorType


@dataclass(kw_only=True)
class ChatErrorAgent:
    """Agent error.

    Attributes:
        type: Error type ("errorAgent").
        agent_error: Agent error information.
    """

    type: str = "errorAgent"
    agent_error: AgentErrorType


@dataclass(kw_only=True)
class ChatErrorStore:
    """Store error.

    Attributes:
        type: Error type ("errorStore").
        store_error: Store error information.
    """

    type: str = "errorStore"
    store_error: StoreErrorType


# Chat error union type
ChatError = Union[ChatErrorChat, ChatErrorAgent, ChatErrorStore]


def ci_content_text(content: CIContent) -> Optional[str]:
    """Get the text content from a chat item content.

    Args:
        content: Chat item content.

    Returns:
        Text content if available, None otherwise.
    """
    if isinstance(content, (CISndMsgContent, CIRcvMsgContent)):
        return content.msg_content.text
    return None
