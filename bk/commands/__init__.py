"""
Simplex messaging system command types.

This package provides a unified interface for all command types in the
Simplex messaging system. It exports:
- All command classes from their respective modules
- A unified SimplexCommand type for use in API calls
- Convenience methods for command construction

This package serves as the main entry point for the SDK's command system,
allowing clients to import all necessary command types from a single location.
"""

from typing import Union

from .base import BaseCommand
from .users import (
    ShowActiveUser,
    CreateActiveUser,
    ListUsers,
    APISetActiveUser,
    APIHideUser,
    APIUnhideUser,
    APIMuteUser,
    APIUnmuteUser,
    APIDeleteUser,
    APIUpdateProfile,
    CreateMyAddress,
    DeleteMyAddress,
    ShowMyAddress,
    SetProfileAddress,
    AddressAutoAccept,
    APICreateMyAddress,
    APIDeleteMyAddress,
    APIShowMyAddress,
    APISetProfileAddress,
    APIAddressAutoAccept,
    Profile,
    LocalProfile,
    AutoAccept,
    UserCommand,
)

from .groups import (
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
    GroupProfile,
    GroupCommand,
)
from .chats import (
    StartChat,
    APIStopChat,
    APIGetChats,
    APIGetChat,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
    ChatCommand,
)
from .messages import (
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
    ComposedMessage,
    MessageCommand,
)
from .files import (
    SetTempFolder,
    SetFilesFolder,
    ReceiveFile,
    CancelFile,
    FileStatus,
    FileCommand,
)
from .database import (
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
    ArchiveConfig,
    DatabaseCommand,
)
from .connections import (
    APIAcceptContact,
    APIRejectContact,
    APISetContactAlias,
    APIContactInfo,
    APIGetContactCode,
    APIVerifyContact,
    AddContact,
    Connect,
    ConnectSimplex,
    APIGetUserProtoServers,
    APISetUserProtoServers,
    ConnectionCommand,
)

# Re-export all enums and data types from base
from .base import (
    ChatType,
    DeleteMode,
    ServerProtocol,
    GroupMemberRole,
    ChatItemId,
    ChatPagination,
    ItemRange,
    ServerCfg,
    MsgContentTag,
    LinkPreview,
    MCBase,
    MCText,
    MCLink,
    MCImage,
    MCFile,
    MCUnknown,
    MsgContent,
)

# Create a unified command type
SimplexCommand = Union[
    UserCommand,
    GroupCommand,
    ChatCommand,
    MessageCommand,
    FileCommand,
    DatabaseCommand,
    ConnectionCommand,
]

__all__ = [
    # Base command
    "BaseCommand",
    # User commands
    "ShowActiveUser",
    "CreateActiveUser",
    "ListUsers",
    "APISetActiveUser",
    "APIHideUser",
    "APIUnhideUser",
    "APIMuteUser",
    "APIUnmuteUser",
    "APIDeleteUser",
    "APIUpdateProfile",
    "CreateMyAddress",
    "DeleteMyAddress",
    "ShowMyAddress",
    "SetProfileAddress",
    "AddressAutoAccept",
    "APICreateMyAddress",
    "APIDeleteMyAddress",
    "APIShowMyAddress",
    "APISetProfileAddress",
    "APIAddressAutoAccept",
    "Profile",
    "LocalProfile",
    "AutoAccept",
    "UserCommand",
    # Group commands
    "NewGroup",
    "APIAddMember",
    "APIJoinGroup",
    "APIRemoveMember",
    "APILeaveGroup",
    "APIListMembers",
    "APIUpdateGroupProfile",
    "APICreateGroupLink",
    "APIGroupLinkMemberRole",
    "APIDeleteGroupLink",
    "APIGetGroupLink",
    "APIGroupMemberInfo",
    "APIGetGroupMemberCode",
    "APIVerifyGroupMember",
    "GroupProfile",
    "GroupCommand",
    # Chat commands
    "StartChat",
    "APIStopChat",
    "APIGetChats",
    "APIGetChat",
    "APIChatRead",
    "APIDeleteChat",
    "APIClearChat",
    "ChatCommand",
    # Message commands
    "APISendMessage",
    "APIUpdateChatItem",
    "APIDeleteChatItem",
    "APIDeleteMemberChatItem",
    "ComposedMessage",
    "MessageCommand",
    # File commands
    "SetTempFolder",
    "SetFilesFolder",
    "ReceiveFile",
    "CancelFile",
    "FileStatus",
    "FileCommand",
    # Database commands
    "APIExportArchive",
    "APIImportArchive",
    "APIDeleteStorage",
    "ArchiveConfig",
    "DatabaseCommand",
    # Connection commands
    "APIAcceptContact",
    "APIRejectContact",
    "APISetContactAlias",
    "APIContactInfo",
    "APIGetContactCode",
    "APIVerifyContact",
    "AddContact",
    "Connect",
    "ConnectSimplex",
    "APIGetUserProtoServers",
    "APISetUserProtoServers",
    "ConnectionCommand",
    # Base types and enums
    "ChatType",
    "DeleteMode",
    "ServerProtocol",
    "GroupMemberRole",
    "ChatItemId",
    "ChatPagination",
    "ItemRange",
    "ServerCfg",
    "MsgContentTag",
    "LinkPreview",
    "MCBase",
    "MCText",
    "MCLink",
    "MCImage",
    "MCFile",
    "MCUnknown",
    "MsgContent",
    # Unified command type
    "SimplexCommand",
]
