"""
Command type definitions for the Simplex messaging system.

This module provides type definitions for all command types and
exports a unified ChatCommand type for use in API calls.
"""

from __future__ import annotations

from typing import Union

# Import all command types
from .commands.base import (
    ChatType,
    DeleteMode,
    GroupMemberRole,
    ServerProtocol,
    Profile,
    GroupProfile,
)

from .commands.user import (
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
)

from .commands.chat import (
    StartChat,
    APIStopChat,
    SetTempFolder,
    SetFilesFolder,
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
    APIGetChats,
    APIGetChat,
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
    APIAcceptContact,
    APIRejectContact,
    APISetContactAlias,
)

from .commands.group import (
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
)

from .commands.file import ReceiveFile, CancelFile, FileStatus

from .commands.misc import (
    SetIncognito,
    AddContact,
    Connect,
    ConnectSimplex,
    APIContactInfo,
    APIGetContactCode,
    APIVerifyContact,
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
    APIGetUserProtoServers,
    APISetUserProtoServers,
)

from .models.message import (
    ComposedMessage,
    MsgContent,
    MCText,
    MCLink,
    MCImage,
    MCFile,
    MCUnknown,
    LinkPreview,
)

from .models.pagination import ChatPagination, ItemRange

from .models.archive import ArchiveConfig, AutoAccept

from .models.server import ServerCfg

# Define the union type for all commands
ChatCommand = Union[
    # User commands
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
    # Chat commands
    StartChat,
    APIStopChat,
    SetTempFolder,
    SetFilesFolder,
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
    APIGetChats,
    APIGetChat,
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
    APIAcceptContact,
    APIRejectContact,
    APISetContactAlias,
    # Group commands
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
    # File commands
    ReceiveFile,
    CancelFile,
    FileStatus,
    # Misc commands
    SetIncognito,
    AddContact,
    Connect,
    ConnectSimplex,
    APIContactInfo,
    APIGetContactCode,
    APIVerifyContact,
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
    APIGetUserProtoServers,
    APISetUserProtoServers,
]
