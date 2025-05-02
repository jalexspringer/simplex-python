"""
Simplex messaging system response types.

This package provides response classes for all Simplex messaging operations,
organized by functional area (users, chats, messages, etc.).
"""

from .base import CommandResponse, CommandError, CommandErrorResponse, CommandErrorType

# User-related responses
from .users import (
    ActiveUserResponse,
    UsersListResponse,
    UserProfileResponse,
    UserProfileUpdatedResponse,
    UserProfileNoChangeResponse,
    UserContactLinkResponse,
    UserContactLinkCreatedResponse,
    UserContactLinkDeletedResponse,
    UserContactLinkUpdatedResponse,
)

# Chat-related responses
from .chats import (
    ChatStartedResponse,
    ChatRunningResponse,
    ChatStoppedResponse,
    ApiChatsResponse,
    ApiCommandResponse,
    ChatReadResponse,
    ChatDeletedResponse,
    ChatClearedResponse,
    NewChatItemsResponse,
    ChatItemUpdatedResponse,
    ChatItemDeletedResponse,
    ChatItemStatusUpdatedResponse,
)

# Message-related responses
from .messages import (
    MessageSentResponse,
    MessageErrorResponse,
    MsgIntegrityErrorResponse,
)

# File-related responses
from .files import (
    RcvFileAcceptedResponse,
    RcvFileStartResponse,
    RcvFileCompleteResponse,
    RcvFileCancelledResponse,
    RcvFileSndCancelledResponse,
    RcvFileAcceptedSndCancelledResponse,
    RcvFileSubErrorResponse,
    SndFileStartResponse,
    SndFileCompleteResponse,
    SndFileCancelledResponse,
    SndFileRcvCancelledResponse,
    SndGroupFileCancelledResponse,
    SndFileSubErrorResponse,
)

# Database-related responses
from .database import (
    ExportArchiveProgressResponse,
    ExportArchiveCompletedResponse,
    ExportArchiveErrorResponse,
    ImportArchiveProgressResponse,
    ImportArchiveCompletedResponse,
    ImportArchiveErrorResponse,
    DeleteStorageCompletedResponse,
    DeleteStorageErrorResponse,
)

# Connection-related responses
from .connections import (
    ContactRequestRejectedResponse,
    ReceivedContactRequestResponse,
    AcceptingContactRequestResponse,
    ContactAlreadyExistsResponse,
    ContactRequestAlreadyAcceptedResponse,
    ContactInfoResponse,
    ContactAliasUpdatedResponse,
    ContactConnectingResponse,
    ContactConnectedResponse,
    ContactUpdatedResponse,
    ContactsMergedResponse,
    ContactDeletedResponse,
    ContactSubErrorResponse,
    ContactSubSummaryResponse,
    ContactsDisconnectedResponse,
    ContactsSubscribedResponse,
    HostConnectedResponse,
    HostDisconnectedResponse,
    UserProtoServersResponse,
    InvitationResponse,
    SentConfirmationResponse,
    SentInvitationResponse,
    ContactConnectionDeletedResponse,
)

# Type alias for all response types
ResponseType = (
    # User responses
    ActiveUserResponse
    | UsersListResponse
    | UserProfileResponse
    | UserProfileUpdatedResponse
    | UserProfileNoChangeResponse
    | UserContactLinkResponse
    | UserContactLinkCreatedResponse
    | UserContactLinkDeletedResponse
    | UserContactLinkUpdatedResponse
    |
    # Chat responses
    ChatStartedResponse
    | ChatRunningResponse
    | ChatStoppedResponse
    | ApiChatsResponse
    | ApiCommandResponse
    | ChatReadResponse
    | ChatDeletedResponse
    | ChatClearedResponse
    | NewChatItemsResponse
    | ChatItemUpdatedResponse
    | ChatItemDeletedResponse
    | ChatItemStatusUpdatedResponse
    |
    # Message responses
    MessageSentResponse
    | MessageErrorResponse
    | MsgIntegrityErrorResponse
    |
    # File responses
    RcvFileAcceptedResponse
    | RcvFileStartResponse
    | RcvFileCompleteResponse
    | RcvFileCancelledResponse
    | RcvFileSndCancelledResponse
    | RcvFileAcceptedSndCancelledResponse
    | RcvFileSubErrorResponse
    | SndFileStartResponse
    | SndFileCompleteResponse
    | SndFileCancelledResponse
    | SndFileRcvCancelledResponse
    | SndGroupFileCancelledResponse
    | SndFileSubErrorResponse
    |
    # Database responses
    ExportArchiveProgressResponse
    | ExportArchiveCompletedResponse
    | ExportArchiveErrorResponse
    | ImportArchiveProgressResponse
    | ImportArchiveCompletedResponse
    | ImportArchiveErrorResponse
    | DeleteStorageCompletedResponse
    | DeleteStorageErrorResponse
    |
    # Connection responses
    ContactRequestRejectedResponse
    | ReceivedContactRequestResponse
    | AcceptingContactRequestResponse
    | ContactAlreadyExistsResponse
    | ContactRequestAlreadyAcceptedResponse
    | ContactInfoResponse
    | ContactAliasUpdatedResponse
    | ContactConnectingResponse
    | ContactConnectedResponse
    | ContactUpdatedResponse
    | ContactsMergedResponse
    | ContactDeletedResponse
    | ContactSubErrorResponse
    | ContactSubSummaryResponse
    | ContactsDisconnectedResponse
    | ContactsSubscribedResponse
    | HostConnectedResponse
    | HostDisconnectedResponse
    | UserProtoServersResponse
    | InvitationResponse
    | SentConfirmationResponse
    | SentInvitationResponse
    | ContactConnectionDeletedResponse
)

__all__ = [
    # User responses
    "ActiveUserResponse",
    "UsersListResponse",
    "UserProfileResponse",
    "UserProfileUpdatedResponse",
    "UserProfileNoChangeResponse",
    "UserContactLinkResponse",
    "UserContactLinkCreatedResponse",
    "UserContactLinkDeletedResponse",
    "UserContactLinkUpdatedResponse",
    # Chat responses
    "ChatStartedResponse",
    "ChatRunningResponse",
    "ChatStoppedResponse",
    "ApiChatsResponse",
    "ApiCommandResponse",
    "ChatReadResponse",
    "ChatDeletedResponse",
    "ChatClearedResponse",
    "NewChatItemsResponse",
    "ChatItemUpdatedResponse",
    "ChatItemDeletedResponse",
    "ChatItemStatusUpdatedResponse",
    # Message responses
    "MessageSentResponse",
    "MessageErrorResponse",
    "MsgIntegrityErrorResponse",
    # File responses
    "RcvFileAcceptedResponse",
    "RcvFileStartResponse",
    "RcvFileCompleteResponse",
    "RcvFileCancelledResponse",
    "RcvFileSndCancelledResponse",
    "RcvFileAcceptedSndCancelledResponse",
    "RcvFileSubErrorResponse",
    "SndFileStartResponse",
    "SndFileCompleteResponse",
    "SndFileCancelledResponse",
    "SndFileRcvCancelledResponse",
    "SndGroupFileCancelledResponse",
    "SndFileSubErrorResponse",
    # Database responses
    "ExportArchiveProgressResponse",
    "ExportArchiveCompletedResponse",
    "ExportArchiveErrorResponse",
    "ImportArchiveProgressResponse",
    "ImportArchiveCompletedResponse",
    "ImportArchiveErrorResponse",
    "DeleteStorageCompletedResponse",
    "DeleteStorageErrorResponse",
    # Connection responses
    "ContactRequestRejectedResponse",
    "ReceivedContactRequestResponse",
    "AcceptingContactRequestResponse",
    "ContactAlreadyExistsResponse",
    "ContactRequestAlreadyAcceptedResponse",
    "ContactInfoResponse",
    "ContactAliasUpdatedResponse",
    "ContactConnectingResponse",
    "ContactConnectedResponse",
    "ContactUpdatedResponse",
    "ContactsMergedResponse",
    "ContactDeletedResponse",
    "ContactSubErrorResponse",
    "ContactSubSummaryResponse",
    "ContactsDisconnectedResponse",
    "ContactsSubscribedResponse",
    "HostConnectedResponse",
    "HostDisconnectedResponse",
    "UserProtoServersResponse",
    "InvitationResponse",
    "SentConfirmationResponse",
    "SentInvitationResponse",
    "ContactConnectionDeletedResponse",
    # Type aliases
    "ResponseType",
]
