"""
Command type definitions for the Simplex messaging system.

This module provides a unified interface for all command types in the
Simplex messaging system. It exports:
- All command classes from their respective modules
- A unified SimplexCommand type for use in API calls
- Convenience methods for command construction

This module serves as the main entry point for the SDK's command system,
allowing clients to import all necessary command types from a single location.
"""

from typing import Union

from .cmds.base import BaseCommand
from .cmds.users import (
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

from .cmds.groups import (
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
from .cmds.chats import (
    StartChat,
    APIStopChat,
    APIGetChats,
    APIGetChat,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
    ChatCommand,
)
from .cmds.messages import (
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
    ComposedMessage,
    MessageCommand,
)
from .cmds.files import (
    SetTempFolder,
    SetFilesFolder,
    ReceiveFile,
    CancelFile,
    FileStatus,
    FileCommand,
)
from .cmds.database import (
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
    ArchiveConfig,
    DatabaseCommand,
)
from .cmds.connections import (
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
from .cmds.base import (
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
