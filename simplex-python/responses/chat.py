"""
Chat-related responses for Simplex messaging system.

This module defines response classes for chat operations and message handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import BaseResponse, ChatResponseType
from ..models.chat import (
    User,
    Chat,
    Contact,
    ChatInfo,
    AChatItem,
    ChatError,
    ConnectionStats,
    UserContactRequest,
    ContactRef,
    ContactSubStatus,
    PendingContactConnection,
    FormattedText,
    MsgErrorType,
)


@dataclass(kw_only=True)
class CRChatStarted(BaseResponse):
    """Response for chat system started.

    Attributes:
        type: Response type identifier ("chatStarted").
    """

    type: str = ChatResponseType.CHAT_STARTED.value


@dataclass(kw_only=True)
class CRChatRunning(BaseResponse):
    """Response for chat system running.

    Attributes:
        type: Response type identifier ("chatRunning").
    """

    type: str = ChatResponseType.CHAT_RUNNING.value


@dataclass(kw_only=True)
class CRChatStopped(BaseResponse):
    """Response for chat system stopped.

    Attributes:
        type: Response type identifier ("chatStopped").
    """

    type: str = ChatResponseType.CHAT_STOPPED.value


@dataclass(kw_only=True)
class CRApiChats(BaseResponse):
    """Response for list of chats.

    Attributes:
        type: Response type identifier ("apiChats").
        user: User information.
        chats: List of chats.
    """

    type: str = ChatResponseType.API_CHATS.value
    user: User
    chats: List[Chat]


@dataclass(kw_only=True)
class CRApiChat(BaseResponse):
    """Response for single chat information.

    Attributes:
        type: Response type identifier ("apiChat").
        user: User information.
        chat: Chat information.
    """

    type: str = ChatResponseType.API_CHAT.value
    user: User
    chat: Chat


@dataclass(kw_only=True)
class CRApiParsedMarkdown(BaseResponse):
    """Response for parsed markdown text.

    Attributes:
        type: Response type identifier ("apiParsedMarkdown").
        formatted_text: Optional formatted text information.
    """

    type: str = ChatResponseType.API_PARSED_MARKDOWN.value
    formatted_text: Optional[List[FormattedText]] = None


@dataclass(kw_only=True)
class CRContactInfo(BaseResponse):
    """Response for contact information.

    Attributes:
        type: Response type identifier ("contactInfo").
        user: User information.
        contact: Contact information.
        connection_stats: Connection statistics.
        custom_user_profile: Optional custom user profile.
    """

    type: str = ChatResponseType.CONTACT_INFO.value
    user: User
    contact: Contact
    connection_stats: ConnectionStats
    custom_user_profile: Optional[dict] = None


@dataclass(kw_only=True)
class CRNewChatItems(BaseResponse):
    """Response for new chat items.

    Attributes:
        type: Response type identifier ("newChatItems").
        user: User information.
        chat_items: List of chat items.
    """

    type: str = ChatResponseType.NEW_CHAT_ITEMS.value
    user: User
    chat_items: List[AChatItem]


@dataclass(kw_only=True)
class CRChatItemStatusUpdated(BaseResponse):
    """Response for updated chat item status.

    Attributes:
        type: Response type identifier ("chatItemStatusUpdated").
        user: User information.
        chat_item: Chat item information.
    """

    type: str = ChatResponseType.CHAT_ITEM_STATUS_UPDATED.value
    user: User
    chat_item: AChatItem


@dataclass(kw_only=True)
class CRChatItemUpdated(BaseResponse):
    """Response for updated chat item.

    Attributes:
        type: Response type identifier ("chatItemUpdated").
        user: User information.
        chat_item: Chat item information.
    """

    type: str = ChatResponseType.CHAT_ITEM_UPDATED.value
    user: User
    chat_item: AChatItem


@dataclass(kw_only=True)
class CRChatItemDeleted(BaseResponse):
    """Response for deleted chat item.

    Attributes:
        type: Response type identifier ("chatItemDeleted").
        user: User information.
        deleted_chat_item: Deleted chat item information.
        to_chat_item: Optional new chat item information.
        by_user: Whether deleted by the user.
    """

    type: str = ChatResponseType.CHAT_ITEM_DELETED.value
    user: User
    deleted_chat_item: AChatItem
    by_user: bool
    to_chat_item: Optional[AChatItem] = None


@dataclass(kw_only=True)
class CRMsgIntegrityError(BaseResponse):
    """Response for message integrity error.

    Attributes:
        type: Response type identifier ("msgIntegrityError").
        user: User information.
        msg_error: Message error information.
    """

    type: str = ChatResponseType.MSG_INTEGRITY_ERROR.value
    user: User
    msg_error: MsgErrorType


@dataclass(kw_only=True)
class CRCmdOk(BaseResponse):
    """Response for successful command execution.

    Attributes:
        type: Response type identifier ("cmdOk").
        user: Optional user information.
    """

    type: str = ChatResponseType.CMD_OK.value
    user_: Optional[User] = None


@dataclass(kw_only=True)
class CRContactRequestRejected(BaseResponse):
    """Response for rejected contact request.

    Attributes:
        type: Response type identifier ("contactRequestRejected").
        user: User information.
        contact_request: Contact request information.
    """

    type: str = ChatResponseType.CONTACT_REQUEST_REJECTED.value
    user: User
    contact_request: UserContactRequest


@dataclass(kw_only=True)
class CRContactAliasUpdated(BaseResponse):
    """Response for updated contact alias.

    Attributes:
        type: Response type identifier ("contactAliasUpdated").
        user: User information.
        to_contact: Updated contact information.
    """

    type: str = ChatResponseType.CONTACT_ALIAS_UPDATED.value
    user: User
    to_contact: Contact


@dataclass(kw_only=True)
class CRInvitation(BaseResponse):
    """Response for invitation.

    Attributes:
        type: Response type identifier ("invitation").
        user: User information.
        conn_req_invitation: Connection request invitation string.
    """

    type: str = ChatResponseType.INVITATION.value
    user: User
    conn_req_invitation: str


@dataclass(kw_only=True)
class CRSentConfirmation(BaseResponse):
    """Response for sent confirmation.

    Attributes:
        type: Response type identifier ("sentConfirmation").
        user: User information.
    """

    type: str = ChatResponseType.SENT_CONFIRMATION.value
    user: User


@dataclass(kw_only=True)
class CRSentInvitation(BaseResponse):
    """Response for sent invitation.

    Attributes:
        type: Response type identifier ("sentInvitation").
        user: User information.
    """

    type: str = ChatResponseType.SENT_INVITATION.value
    user: User


@dataclass(kw_only=True)
class CRContactUpdated(BaseResponse):
    """Response for updated contact.

    Attributes:
        type: Response type identifier ("contactUpdated").
        user: User information.
        from_contact: Original contact information.
        to_contact: Updated contact information.
    """

    type: str = ChatResponseType.CONTACT_UPDATED.value
    user: User
    from_contact: Contact
    to_contact: Contact


@dataclass(kw_only=True)
class CRContactsMerged(BaseResponse):
    """Response for merged contacts.

    Attributes:
        type: Response type identifier ("contactsMerged").
        user: User information.
        into_contact: Target contact information.
        merged_contact: Source contact information.
    """

    type: str = ChatResponseType.CONTACTS_MERGED.value
    user: User
    into_contact: Contact
    merged_contact: Contact


@dataclass(kw_only=True)
class CRContactDeleted(BaseResponse):
    """Response for deleted contact.

    Attributes:
        type: Response type identifier ("contactDeleted").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.CONTACT_DELETED.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRChatCleared(BaseResponse):
    """Response for cleared chat.

    Attributes:
        type: Response type identifier ("chatCleared").
        user: User information.
        chat_info: Chat information.
    """

    type: str = ChatResponseType.CHAT_CLEARED.value
    user: User
    chat_info: ChatInfo


@dataclass(kw_only=True)
class CRReceivedContactRequest(BaseResponse):
    """Response for received contact request.

    Attributes:
        type: Response type identifier ("receivedContactRequest").
        user: User information.
        contact_request: Contact request information.
    """

    type: str = ChatResponseType.RECEIVED_CONTACT_REQUEST.value
    user: User
    contact_request: UserContactRequest


@dataclass(kw_only=True)
class CRAcceptingContactRequest(BaseResponse):
    """Response for accepting contact request.

    Attributes:
        type: Response type identifier ("acceptingContactRequest").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.ACCEPTING_CONTACT_REQUEST.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRContactAlreadyExists(BaseResponse):
    """Response for contact already exists.

    Attributes:
        type: Response type identifier ("contactAlreadyExists").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.CONTACT_ALREADY_EXISTS.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRContactRequestAlreadyAccepted(BaseResponse):
    """Response for contact request already accepted.

    Attributes:
        type: Response type identifier ("contactRequestAlreadyAccepted").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.CONTACT_REQUEST_ALREADY_ACCEPTED.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRContactConnecting(BaseResponse):
    """Response for contact connecting.

    Attributes:
        type: Response type identifier ("contactConnecting").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.CONTACT_CONNECTING.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRContactConnected(BaseResponse):
    """Response for contact connected.

    Attributes:
        type: Response type identifier ("contactConnected").
        user: User information.
        contact: Contact information.
        user_custom_profile: Optional custom user profile.
    """

    type: str = ChatResponseType.CONTACT_CONNECTED.value
    user: User
    contact: Contact
    user_custom_profile: Optional[dict] = None


@dataclass(kw_only=True)
class CRContactAnotherClient(BaseResponse):
    """Response for contact from another client.

    Attributes:
        type: Response type identifier ("contactAnotherClient").
        user: User information.
        contact: Contact information.
    """

    type: str = ChatResponseType.CONTACT_ANOTHER_CLIENT.value
    user: User
    contact: Contact


@dataclass(kw_only=True)
class CRContactSubError(BaseResponse):
    """Response for contact subscription error.

    Attributes:
        type: Response type identifier ("contactSubError").
        user: User information.
        contact: Contact information.
        chat_error: Chat error information.
    """

    type: str = ChatResponseType.CONTACT_SUB_ERROR.value
    user: User
    contact: Contact
    chat_error: ChatError


@dataclass(kw_only=True)
class CRContactSubSummary(BaseResponse):
    """Response for contact subscription summary.

    Attributes:
        type: Response type identifier ("contactSubSummary").
        user: User information.
        contact_subscriptions: List of contact subscription status.
    """

    type: str = ChatResponseType.CONTACT_SUB_SUMMARY.value
    user: User
    contact_subscriptions: List[ContactSubStatus]


@dataclass(kw_only=True)
class CRContactsDisconnected(BaseResponse):
    """Response for disconnected contacts.

    Attributes:
        type: Response type identifier ("contactsDisconnected").
        user: User information.
        server: Server identifier.
        contact_refs: List of contact references.
    """

    type: str = ChatResponseType.CONTACTS_DISCONNECTED.value
    user: User
    server: str
    contact_refs: List[ContactRef]


@dataclass(kw_only=True)
class CRContactsSubscribed(BaseResponse):
    """Response for subscribed contacts.

    Attributes:
        type: Response type identifier ("contactsSubscribed").
        user: User information.
        server: Server identifier.
        contact_refs: List of contact references.
    """

    type: str = ChatResponseType.CONTACTS_SUBSCRIBED.value
    user: User
    server: str
    contact_refs: List[ContactRef]


@dataclass(kw_only=True)
class CRHostConnected(BaseResponse):
    """Response for host connected.

    Attributes:
        type: Response type identifier ("hostConnected").
        protocol: Protocol identifier.
        transport_host: Transport host identifier.
    """

    type: str = ChatResponseType.HOST_CONNECTED.value
    protocol: str
    transport_host: str


@dataclass(kw_only=True)
class CRHostDisconnected(BaseResponse):
    """Response for host disconnected.

    Attributes:
        type: Response type identifier ("hostDisconnected").
        protocol: Protocol identifier.
        transport_host: Transport host identifier.
    """

    type: str = ChatResponseType.HOST_DISCONNECTED.value
    protocol: str
    transport_host: str


@dataclass(kw_only=True)
class CRContactConnectionDeleted(BaseResponse):
    """Response for deleted contact connection.

    Attributes:
        type: Response type identifier ("contactConnectionDeleted").
        user: User information.
        connection: Pending contact connection information.
    """

    type: str = ChatResponseType.CONTACT_CONNECTION_DELETED.value
    user: User
    connection: PendingContactConnection
