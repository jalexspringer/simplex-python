"""
Simplex messaging system response types.

This package provides response classes for all Simplex messaging operations,
organized by functional area (users, chats, messages, etc.).
"""

from .base import (
    CommandResponse,
    CommandError,
    CommandErrorResponse,
    CommandErrorType,
    ApiParsedMarkdownResponse,
    CmdOkResponse,
    ResponseFactory,
)

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
    UserContactLinkSubscribedResponse,
    UserContactLinkSubErrorResponse,
)

from .groups import (
    GroupCreatedResponse,
    GroupMembersResponse,
    UserAcceptedGroupSentResponse,
    UserDeletedMemberResponse,
    SentGroupInvitationResponse,
    LeftMemberUserResponse,
    GroupDeletedUserResponse,
    GroupInvitationResponse,
    ReceivedGroupInvitationResponse,
    UserJoinedGroupResponse,
    JoinedGroupMemberResponse,
    JoinedGroupMemberConnectingResponse,
    ConnectedToGroupMemberResponse,
    DeletedMemberResponse,
    DeletedMemberUserResponse,
    LeftMemberResponse,
    GroupRemovedResponse,
    GroupDeletedResponse,
    GroupUpdatedResponse,
    GroupEmptyResponse,
    MemberSubErrorResponse,
    MemberSubSummaryResponse,
    GroupSubscribedResponse,
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

# Define domain-specific response type unions for better type hints
UserResponse = (
    ActiveUserResponse
    | UsersListResponse
    | UserProfileResponse
    | UserProfileUpdatedResponse
    | UserProfileNoChangeResponse
    | UserContactLinkResponse
    | UserContactLinkCreatedResponse
    | UserContactLinkDeletedResponse
    | UserContactLinkUpdatedResponse
    | UserContactLinkSubscribedResponse
    | UserContactLinkSubErrorResponse
    | None
)

GroupResponse = (
    GroupCreatedResponse
    | GroupMembersResponse
    | UserAcceptedGroupSentResponse
    | UserDeletedMemberResponse
    | SentGroupInvitationResponse
    | LeftMemberUserResponse
    | GroupDeletedUserResponse
    | GroupInvitationResponse
    | ReceivedGroupInvitationResponse
    | UserJoinedGroupResponse
    | JoinedGroupMemberResponse
    | JoinedGroupMemberConnectingResponse
    | ConnectedToGroupMemberResponse
    | DeletedMemberResponse
    | DeletedMemberUserResponse
    | LeftMemberResponse
    | GroupRemovedResponse
    | GroupDeletedResponse
    | GroupUpdatedResponse
    | GroupEmptyResponse
    | MemberSubErrorResponse
    | MemberSubSummaryResponse
    | GroupSubscribedResponse
    | None
)

ChatResponse = (
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
    | None
)

MessageResponse = (
    MessageSentResponse | MessageErrorResponse | MsgIntegrityErrorResponse | None
)

FileResponse = (
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
    | None
)

DatabaseResponse = (
    ExportArchiveProgressResponse
    | ExportArchiveCompletedResponse
    | ExportArchiveErrorResponse
    | ImportArchiveProgressResponse
    | ImportArchiveCompletedResponse
    | ImportArchiveErrorResponse
    | DeleteStorageCompletedResponse
    | DeleteStorageErrorResponse
    | None
)

ConnectionResponse = (
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
    | None
)


# Register response types with the factory
def _register_response_types():
    """Register all response types with the ResponseFactory."""
    # User responses
    ResponseFactory.register_response_type("activeUser", ActiveUserResponse)
    ResponseFactory.register_response_type("users", UsersListResponse)
    ResponseFactory.register_response_type("userProfile", UserProfileResponse)
    ResponseFactory.register_response_type(
        "userProfileUpdated", UserProfileUpdatedResponse
    )
    ResponseFactory.register_response_type(
        "userProfileNoChange", UserProfileNoChangeResponse
    )
    ResponseFactory.register_response_type("userContactLink", UserContactLinkResponse)
    ResponseFactory.register_response_type(
        "userContactLinkCreated", UserContactLinkCreatedResponse
    )
    ResponseFactory.register_response_type(
        "userContactLinkDeleted", UserContactLinkDeletedResponse
    )
    ResponseFactory.register_response_type(
        "userContactLinkUpdated", UserContactLinkUpdatedResponse
    )
    ResponseFactory.register_response_type(
        "subscribed", UserContactLinkSubscribedResponse
    )
    ResponseFactory.register_response_type("subError", UserContactLinkSubErrorResponse)

    # Group responses
    ResponseFactory.register_response_type("groupCreated", GroupCreatedResponse)
    ResponseFactory.register_response_type("groupMembers", GroupMembersResponse)
    ResponseFactory.register_response_type(
        "userAcceptedGroupSent", UserAcceptedGroupSentResponse
    )
    ResponseFactory.register_response_type(
        "userDeletedMember", UserDeletedMemberResponse
    )
    ResponseFactory.register_response_type(
        "sentGroupInvitation", SentGroupInvitationResponse
    )
    ResponseFactory.register_response_type("leftMemberUser", LeftMemberUserResponse)
    ResponseFactory.register_response_type("groupDeletedUser", GroupDeletedUserResponse)
    ResponseFactory.register_response_type("groupInvitation", GroupInvitationResponse)
    ResponseFactory.register_response_type(
        "receivedGroupInvitation", ReceivedGroupInvitationResponse
    )
    ResponseFactory.register_response_type("userJoinedGroup", UserJoinedGroupResponse)
    ResponseFactory.register_response_type(
        "joinedGroupMember", JoinedGroupMemberResponse
    )
    ResponseFactory.register_response_type(
        "joinedGroupMemberConnecting", JoinedGroupMemberConnectingResponse
    )
    ResponseFactory.register_response_type(
        "connectedToGroupMember", ConnectedToGroupMemberResponse
    )
    ResponseFactory.register_response_type("deletedMember", DeletedMemberResponse)
    ResponseFactory.register_response_type(
        "deletedMemberUser", DeletedMemberUserResponse
    )
    ResponseFactory.register_response_type("leftMember", LeftMemberResponse)
    ResponseFactory.register_response_type("groupRemoved", GroupRemovedResponse)
    ResponseFactory.register_response_type("groupDeleted", GroupDeletedResponse)
    ResponseFactory.register_response_type("groupUpdated", GroupUpdatedResponse)
    ResponseFactory.register_response_type("groupEmpty", GroupEmptyResponse)
    ResponseFactory.register_response_type("memberSubError", MemberSubErrorResponse)
    ResponseFactory.register_response_type("memberSubSummary", MemberSubSummaryResponse)
    ResponseFactory.register_response_type("groupSubscribed", GroupSubscribedResponse)

    # Chat responses
    ResponseFactory.register_response_type("chatStarted", ChatStartedResponse)
    ResponseFactory.register_response_type("chatRunning", ChatRunningResponse)
    ResponseFactory.register_response_type("chatStopped", ChatStoppedResponse)
    ResponseFactory.register_response_type("apiChats", ApiChatsResponse)
    ResponseFactory.register_response_type("apiCommand", ApiCommandResponse)
    ResponseFactory.register_response_type("chatRead", ChatReadResponse)
    ResponseFactory.register_response_type("chatDeleted", ChatDeletedResponse)
    ResponseFactory.register_response_type("chatCleared", ChatClearedResponse)
    ResponseFactory.register_response_type("newChatItems", NewChatItemsResponse)
    ResponseFactory.register_response_type("chatItemUpdated", ChatItemUpdatedResponse)
    ResponseFactory.register_response_type("chatItemDeleted", ChatItemDeletedResponse)
    ResponseFactory.register_response_type(
        "chatItemStatusUpdated", ChatItemStatusUpdatedResponse
    )

    # Message responses
    ResponseFactory.register_response_type("messageSent", MessageSentResponse)
    ResponseFactory.register_response_type("messageError", MessageErrorResponse)
    ResponseFactory.register_response_type(
        "msgIntegrityError", MsgIntegrityErrorResponse
    )

    # File responses
    ResponseFactory.register_response_type("rcvFileAccepted", RcvFileAcceptedResponse)
    ResponseFactory.register_response_type("rcvFileStart", RcvFileStartResponse)
    ResponseFactory.register_response_type("rcvFileComplete", RcvFileCompleteResponse)
    ResponseFactory.register_response_type("rcvFileCancelled", RcvFileCancelledResponse)
    ResponseFactory.register_response_type(
        "rcvFileSndCancelled", RcvFileSndCancelledResponse
    )
    ResponseFactory.register_response_type(
        "rcvFileAcceptedSndCancelled", RcvFileAcceptedSndCancelledResponse
    )
    ResponseFactory.register_response_type("rcvFileSubError", RcvFileSubErrorResponse)
    ResponseFactory.register_response_type("sndFileStart", SndFileStartResponse)
    ResponseFactory.register_response_type("sndFileComplete", SndFileCompleteResponse)
    ResponseFactory.register_response_type("sndFileCancelled", SndFileCancelledResponse)
    ResponseFactory.register_response_type(
        "sndFileRcvCancelled", SndFileRcvCancelledResponse
    )
    ResponseFactory.register_response_type(
        "sndGroupFileCancelled", SndGroupFileCancelledResponse
    )
    ResponseFactory.register_response_type("sndFileSubError", SndFileSubErrorResponse)

    # Database responses
    ResponseFactory.register_response_type(
        "exportArchiveProgress", ExportArchiveProgressResponse
    )
    ResponseFactory.register_response_type(
        "exportArchiveCompleted", ExportArchiveCompletedResponse
    )
    ResponseFactory.register_response_type(
        "exportArchiveError", ExportArchiveErrorResponse
    )
    ResponseFactory.register_response_type(
        "importArchiveProgress", ImportArchiveProgressResponse
    )
    ResponseFactory.register_response_type(
        "importArchiveCompleted", ImportArchiveCompletedResponse
    )
    ResponseFactory.register_response_type(
        "importArchiveError", ImportArchiveErrorResponse
    )
    ResponseFactory.register_response_type(
        "deleteStorageCompleted", DeleteStorageCompletedResponse
    )
    ResponseFactory.register_response_type(
        "deleteStorageError", DeleteStorageErrorResponse
    )

    # Connection responses
    ResponseFactory.register_response_type(
        "contactRequestRejected", ContactRequestRejectedResponse
    )
    ResponseFactory.register_response_type(
        "receivedContactRequest", ReceivedContactRequestResponse
    )
    ResponseFactory.register_response_type(
        "acceptingContactRequest", AcceptingContactRequestResponse
    )
    ResponseFactory.register_response_type(
        "contactAlreadyExists", ContactAlreadyExistsResponse
    )
    ResponseFactory.register_response_type(
        "contactRequestAlreadyAccepted", ContactRequestAlreadyAcceptedResponse
    )
    ResponseFactory.register_response_type("contactInfo", ContactInfoResponse)
    ResponseFactory.register_response_type(
        "contactAliasUpdated", ContactAliasUpdatedResponse
    )
    ResponseFactory.register_response_type(
        "contactConnecting", ContactConnectingResponse
    )
    ResponseFactory.register_response_type("contactConnected", ContactConnectedResponse)
    ResponseFactory.register_response_type("contactUpdated", ContactUpdatedResponse)
    ResponseFactory.register_response_type("contactsMerged", ContactsMergedResponse)
    ResponseFactory.register_response_type("contactDeleted", ContactDeletedResponse)
    ResponseFactory.register_response_type("contactSubError", ContactSubErrorResponse)
    ResponseFactory.register_response_type(
        "contactSubSummary", ContactSubSummaryResponse
    )
    ResponseFactory.register_response_type(
        "contactsDisconnected", ContactsDisconnectedResponse
    )
    ResponseFactory.register_response_type(
        "contactsSubscribed", ContactsSubscribedResponse
    )
    ResponseFactory.register_response_type("hostConnected", HostConnectedResponse)
    ResponseFactory.register_response_type("hostDisconnected", HostDisconnectedResponse)
    ResponseFactory.register_response_type("userProtoServers", UserProtoServersResponse)
    ResponseFactory.register_response_type("invitation", InvitationResponse)
    ResponseFactory.register_response_type("sentConfirmation", SentConfirmationResponse)
    ResponseFactory.register_response_type("sentInvitation", SentInvitationResponse)
    ResponseFactory.register_response_type(
        "contactConnectionDeleted", ContactConnectionDeletedResponse
    )


# Register all response types when this module is imported
_register_response_types()

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
    | UserContactLinkSubscribedResponse
    | UserContactLinkSubErrorResponse
    |
    # Group responses
    GroupCreatedResponse
    | GroupMembersResponse
    | UserAcceptedGroupSentResponse
    | UserDeletedMemberResponse
    | SentGroupInvitationResponse
    | LeftMemberUserResponse
    | GroupDeletedUserResponse
    | GroupInvitationResponse
    | ReceivedGroupInvitationResponse
    | UserJoinedGroupResponse
    | JoinedGroupMemberResponse
    | JoinedGroupMemberConnectingResponse
    | ConnectedToGroupMemberResponse
    | DeletedMemberResponse
    | DeletedMemberUserResponse
    | LeftMemberResponse
    | GroupRemovedResponse
    | GroupDeletedResponse
    | GroupUpdatedResponse
    | GroupEmptyResponse
    | MemberSubErrorResponse
    | MemberSubSummaryResponse
    | GroupSubscribedResponse
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
    | CmdOkResponse
    | ApiParsedMarkdownResponse
    | CommandResponse
    | CommandError
    | CommandErrorResponse
    | CommandErrorType
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
    "UserContactLinkSubscribedResponse",
    "UserContactLinkSubErrorResponse",
    # Group responses
    "GroupCreatedResponse",
    "GroupMembersResponse",
    "UserAcceptedGroupSentResponse",
    "UserDeletedMemberResponse",
    "SentGroupInvitationResponse",
    "LeftMemberUserResponse",
    "GroupDeletedUserResponse",
    "GroupInvitationResponse",
    "ReceivedGroupInvitationResponse",
    "UserJoinedGroupResponse",
    "JoinedGroupMemberResponse",
    "JoinedGroupMemberConnectingResponse",
    "ConnectedToGroupMemberResponse",
    "DeletedMemberResponse",
    "DeletedMemberUserResponse",
    "LeftMemberResponse",
    "GroupRemovedResponse",
    "GroupDeletedResponse",
    "GroupUpdatedResponse",
    "GroupEmptyResponse",
    "MemberSubErrorResponse",
    "MemberSubSummaryResponse",
    "GroupSubscribedResponse",
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
    "CommandResponse",
    "CommandError",
    "CommandErrorResponse",
    "CommandErrorType",
    "ApiParsedMarkdownResponse",
    "CmdOkResponse",
    "UserResponse",
    "GroupResponse",
    "ChatResponse",
    "MessageResponse",
    "FileResponse",
    "DatabaseResponse",
    "ConnectionResponse",
]
