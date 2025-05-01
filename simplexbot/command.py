"""
Command types, enums, and dataclasses for the Simplex Python client.

Each command is represented as a dataclass with type hints and
docstrings, suitable for serialization and use with the Simplex WebSocket API.

All types follow Python 3.13+ idioms and best practices.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class ChatType(Enum):
    """Enumeration of chat types.

    Attributes:
        DIRECT: Direct (one-to-one) chat.
        GROUP: Group chat.
        CONTACT_REQUEST: Contact request chat.
    """

    DIRECT = "@"
    GROUP = "#"
    CONTACT_REQUEST = "<@"


class DeleteMode(Enum):
    """Enumeration of chat item deletion modes.

    Attributes:
        BROADCAST: Delete for all participants (broadcast).
        INTERNAL: Delete only locally (internal).
    """

    BROADCAST = "broadcast"
    INTERNAL = "internal"


class GroupMemberRole(Enum):
    """Enumeration of group member roles.

    Attributes:
        MEMBER: Regular group member.
        ADMIN: Group administrator.
        OWNER: Group owner.
    """

    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"


@dataclass(kw_only=True)
class Profile:
    """User profile information.

    Attributes:
        display_name: The user's display name.
        full_name: The user's full name.
        image: Optional URL/path to the user's avatar image.
        contact_link: Optional contact link for the user.
    """

    display_name: str
    full_name: str
    image: Optional[str] = None
    contact_link: Optional[str] = None


@dataclass(kw_only=True)
class ShowActiveUser:
    """Command to show the active user profile.

    Attributes:
        type: Discriminator for this command ("showActiveUser").
    """

    type: str = "showActiveUser"


@dataclass(kw_only=True)
class CreateActiveUser:
    """Command to create a new active user.

    Attributes:
        type: Discriminator for this command ("createActiveUser").
        profile: Optional profile information for the new user.
        same_servers: Whether to use the same servers as before.
        past_timestamp: Whether to use a past timestamp for creation.
    """

    type: str = "createActiveUser"
    profile: Optional[Profile] = None
    same_servers: bool = True
    past_timestamp: bool = False


@dataclass(kw_only=True)
class ListUsers:
    """Command to list all users.

    Attributes:
        type: Discriminator for this command ("listUsers").
    """

    type: str = "listUsers"


@dataclass(kw_only=True)
class APISetActiveUser:
    """Command to set the active user for the API.

    Attributes:
        type: Discriminator for this command ("apiSetActiveUser").
        user_id: The user's unique identifier.
        view_pwd: Optional password required to view the user.
    """

    type: str = "apiSetActiveUser"
    user_id: int
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class APIHideUser:
    """Command to hide a user in the system.

    Attributes:
        type: Discriminator for this command ("apiHideUser").
        user_id: ID of the user to hide.
        view_pwd: Password required to view the user.
    """

    type: str = "apiHideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIUnhideUser:
    """Command to unhide a user in the system.

    Attributes:
        type: Discriminator for this command ("apiUnhideUser").
        user_id: ID of the user to unhide.
        view_pwd: Password required to view the user.
    """

    type: str = "apiUnhideUser"
    user_id: int
    view_pwd: str


@dataclass(kw_only=True)
class APIMuteUser:
    """Command to mute a user in the system.

    Attributes:
        type: Discriminator for this command ("apiMuteUser").
        user_id: ID of the user to mute.
    """

    type: str = "apiMuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIUnmuteUser:
    """Command to unmute a user in the system.

    Attributes:
        type: Discriminator for this command ("apiUnmuteUser").
        user_id: ID of the user to unmute.
    """

    type: str = "apiUnmuteUser"
    user_id: int


@dataclass(kw_only=True)
class APIDeleteUser:
    """Command to delete a user from the system.

    Attributes:
        type: Discriminator for this command ("apiDeleteUser").
        user_id: ID of the user to delete.
        del_smp_queues: Whether to delete SMP queues.
        view_pwd: Optional password required to view the user.
    """

    type: str = "apiDeleteUser"
    user_id: int
    del_smp_queues: bool
    view_pwd: Optional[str] = None


@dataclass(kw_only=True)
class StartChat:
    """Command to start a new chat session.

    Attributes:
        type: Discriminator for this command ("startChat").
        subscribe_connections: Whether to subscribe to connection updates.
        enable_expire_chat_items: Whether to enable expiring chat items.
        start_xftp_workers: Whether to start XFTP workers.
    """

    type: str = "startChat"
    subscribe_connections: Optional[bool] = None
    enable_expire_chat_items: Optional[bool] = None
    start_xftp_workers: Optional[bool] = None


@dataclass(kw_only=True)
class APIStopChat:
    """Command to stop a chat session.

    Attributes:
        type: Discriminator for this command ("apiStopChat").
    """

    type: str = "apiStopChat"


@dataclass(kw_only=True)
class SetTempFolder:
    """Command to set the temporary folder path.

    Attributes:
        type: Discriminator for this command ("setTempFolder").
        temp_folder: Path to the temporary folder.
    """

    type: str = "setTempFolder"
    temp_folder: str


@dataclass(kw_only=True)
class SetFilesFolder:
    """Command to set the files folder path.

    Attributes:
        type: Discriminator for this command ("setFilesFolder").
        file_path: Path to the files folder.
    """

    type: str = "setFilesFolder"
    file_path: str


@dataclass(kw_only=True)
class SetIncognito:
    """Command to enable or disable incognito mode.

    Attributes:
        type: Discriminator for this command ("setIncognito").
        incognito: Whether to enable incognito mode.
    """

    type: str = "setIncognito"
    incognito: bool


@dataclass(kw_only=True)
class ArchiveConfig:
    """Configuration for chat archive import/export.

    Attributes:
        archive_path: Path to the archive file.
        disable_compression: Whether to disable compression.
        parent_temp_directory: Parent directory for temporary files.
    """

    archive_path: str
    disable_compression: Optional[bool] = None
    parent_temp_directory: Optional[str] = None


@dataclass(kw_only=True)
class APIExportArchive:
    """Command to export the chat archive.

    Attributes:
        type: Discriminator for this command ("apiExportArchive").
        config: Archive configuration.
    """

    type: str = "apiExportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIImportArchive:
    """Command to import a chat archive.

    Attributes:
        type: Discriminator for this command ("apiImportArchive").
        config: Archive configuration.
    """

    type: str = "apiImportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIDeleteStorage:
    """Command to delete user storage.

    Attributes:
        type: Discriminator for this command ("apiDeleteStorage").
    """

    type: str = "apiDeleteStorage"


@dataclass(kw_only=True)
class ChatPagination:
    """Pagination parameters for chat queries.

    Attributes:
        count: Number of items to retrieve.
        after: Optional ID to start after.
        before: Optional ID to end before.
    """

    count: int
    after: Optional[int] = None
    before: Optional[int] = None


@dataclass(kw_only=True)
class APIGetChats:
    """Command to retrieve a list of chats.

    Attributes:
        type: Discriminator for this command ("apiGetChats").
        user_id: ID of the user.
        pending_connections: Whether to include pending connections.
    """

    type: str = "apiGetChats"
    user_id: int
    pending_connections: Optional[bool] = None


@dataclass(kw_only=True)
class APIGetChat:
    """Command to retrieve a specific chat.

    Attributes:
        type: Discriminator for this command ("apiGetChat").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
        pagination: Pagination parameters.
        search: Optional search string.
    """

    type: str = "apiGetChat"
    chat_type: ChatType
    chat_id: int
    pagination: ChatPagination
    search: Optional[str] = None


@dataclass(kw_only=True)
class MsgContent:
    """Message content for chat items (variant placeholder).

    Attributes:
        type: Message content type.
        text: Optional text content.
    """

    type: str
    text: Optional[str] = None


@dataclass(kw_only=True)
class ComposedMessage:
    """Composed message object for sending.

    Attributes:
        msg_content: The message content object.
        file_path: Optional file path to attach.
        quoted_item_id: Optional ID of quoted chat item.
    """

    msg_content: MsgContent
    file_path: Optional[str] = None
    quoted_item_id: Optional[int] = None


@dataclass(kw_only=True)
class APISendMessage:
    """Command to send a message in a chat.

    Attributes:
        type: Discriminator for this command ("apiSendMessage").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
        messages: List of composed messages to send.
    """

    type: str = "apiSendMessage"
    chat_type: ChatType
    chat_id: int
    messages: List[ComposedMessage]


@dataclass(kw_only=True)
class APIUpdateChatItem:
    """Command to update a chat item.

    Attributes:
        type: Discriminator for this command ("apiUpdateChatItem").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
        chat_item_id: The ID of the chat item to update.
        msg_content: The new message content.
    """

    type: str = "apiUpdateChatItem"
    chat_type: ChatType
    chat_id: int
    chat_item_id: int
    msg_content: MsgContent


@dataclass(kw_only=True)
class APIDeleteChatItem:
    """Command to delete a chat item.

    Attributes:
        type: Discriminator for this command ("apiDeleteChatItem").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
        chat_item_id: The ID of the chat item to delete.
        delete_mode: Deletion mode (broadcast/internal).
    """

    type: str = "apiDeleteChatItem"
    chat_type: ChatType
    chat_id: int
    chat_item_id: int
    delete_mode: DeleteMode


@dataclass(kw_only=True)
class APIDeleteMemberChatItem:
    """Command to delete a group member's chat item.

    Attributes:
        type: Discriminator for this command ("apiDeleteMemberChatItem").
        group_id: Group identifier.
        group_member_id: Member identifier.
        item_id: Item identifier.
    """

    type: str = "apiDeleteMemberChatItem"
    group_id: int
    group_member_id: int
    item_id: int


@dataclass(kw_only=True)
class APIChatRead:
    """Command to mark chat items as read.

    Attributes:
        type: Discriminator for this command ("apiChatRead").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
        item_range: Optional tuple (start, end) of item IDs.
    """

    type: str = "apiChatRead"
    chat_type: ChatType
    chat_id: int
    item_range: Optional[Tuple[int, int]] = None


@dataclass(kw_only=True)
class APIDeleteChat:
    """Command to delete a chat.

    Attributes:
        type: Discriminator for this command ("apiDeleteChat").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
    """

    type: str = "apiDeleteChat"
    chat_type: ChatType
    chat_id: int


@dataclass(kw_only=True)
class APIClearChat:
    """Command to clear all items in a chat.

    Attributes:
        type: Discriminator for this command ("apiClearChat").
        chat_type: The type of chat.
        chat_id: The chat's unique identifier.
    """

    type: str = "apiClearChat"
    chat_type: ChatType
    chat_id: int


@dataclass(kw_only=True)
class APIAcceptContact:
    """Command to accept a contact request.

    Attributes:
        type: Discriminator for this command ("apiAcceptContact").
        contact_req_id: The contact request identifier.
    """

    type: str = "apiAcceptContact"
    contact_req_id: int


@dataclass(kw_only=True)
class APIRejectContact:
    """Command to reject a contact request.

    Attributes:
        type: Discriminator for this command ("apiRejectContact").
        contact_req_id: The contact request identifier.
    """

    type: str = "apiRejectContact"
    contact_req_id: int


@dataclass(kw_only=True)
class APIUpdateProfile:
    """Command to update a user's profile.

    Attributes:
        type: Discriminator for this command ("apiUpdateProfile").
        user_id: The user's unique identifier.
        profile: The new profile object.
    """

    type: str = "apiUpdateProfile"
    user_id: int
    profile: Profile


@dataclass(kw_only=True)
class APISetContactAlias:
    """Command to set a local alias for a contact.

    Attributes:
        type: Discriminator for this command ("apiSetContactAlias").
        contact_id: The contact's unique identifier.
        local_alias: The alias string to set.
    """

    type: str = "apiSetContactAlias"
    contact_id: int
    local_alias: str


@dataclass(kw_only=True)
class GroupProfile:
    """Profile for a group chat.

    Attributes:
        display_name: Display name for the group.
        full_name: Full name for the group.
        image: Optional group image URL or path.
    """

    display_name: str
    full_name: str
    image: Optional[str] = None


@dataclass(kw_only=True)
class NewGroup:
    """Command to create a new group chat.

    Attributes:
        type: Discriminator for this command ("newGroup").
        group_profile: The profile for the new group.
    """

    type: str = "newGroup"
    group_profile: GroupProfile


@dataclass(kw_only=True)
class APIAddMember:
    """Command to add a member to a group chat.

    Attributes:
        type: Discriminator for this command ("apiAddMember").
        group_id: The group identifier.
        contact_id: The contact identifier.
        member_role: The role to assign to the new member.
    """

    type: str = "apiAddMember"
    group_id: int
    contact_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIJoinGroup:
    """Command to join a group chat.

    Attributes:
        type: Discriminator for this command ("apiJoinGroup").
        group_id: The group identifier.
    """

    type: str = "apiJoinGroup"
    group_id: int


@dataclass(kw_only=True)
class APIRemoveMember:
    """Command to remove a member from a group chat.

    Attributes:
        type: Discriminator for this command ("apiRemoveMember").
        group_id: The group identifier.
        member_id: The member identifier.
    """

    type: str = "apiRemoveMember"
    group_id: int
    member_id: int


@dataclass(kw_only=True)
class APILeaveGroup:
    """Command to leave a group chat.

    Attributes:
        type: Discriminator for this command ("apiLeaveGroup").
        group_id: The group identifier.
    """

    type: str = "apiLeaveGroup"
    group_id: int


@dataclass(kw_only=True)
class APIListMembers:
    """Command to list all members of a group chat.

    Attributes:
        type: Discriminator for this command ("apiListMembers").
        group_id: The group identifier.
    """

    type: str = "apiListMembers"
    group_id: int


@dataclass(kw_only=True)
class APIUpdateGroupProfile:
    """Command to update the profile of a group chat.

    Attributes:
        type: Discriminator for this command ("apiUpdateGroupProfile").
        group_id: The group identifier.
        group_profile: The new group profile.
    """

    type: str = "apiUpdateGroupProfile"
    group_id: int
    group_profile: GroupProfile


@dataclass(kw_only=True)
class APICreateGroupLink:
    """Command to create a group link for inviting members.

    Attributes:
        type: Discriminator for this command ("apiCreateGroupLink").
        group_id: The group identifier.
        member_role: The role for invited members.
    """

    type: str = "apiCreateGroupLink"
    group_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIGroupLinkMemberRole:
    """Command to set the member role for a group link.

    Attributes:
        type: Discriminator for this command ("apiGroupLinkMemberRole").
        group_id: The group identifier.
        member_role: The member role to set.
    """

    type: str = "apiGroupLinkMemberRole"
    group_id: int
    member_role: GroupMemberRole


@dataclass(kw_only=True)
class APIDeleteGroupLink:
    """Command to delete a group link.

    Attributes:
        type: Discriminator for this command ("apiDeleteGroupLink").
        group_id: The group identifier.
    """

    type: str = "apiDeleteGroupLink"
    group_id: int


@dataclass(kw_only=True)
class APIGetGroupLink:
    """Command to retrieve a group link.

    Attributes:
        type: Discriminator for this command ("apiGetGroupLink").
        group_id: The group identifier.
    """

    type: str = "apiGetGroupLink"
    group_id: int


@dataclass(kw_only=True)
class CreateMyAddress:
    """Command to create a new address for the user.

    Attributes:
        type: Discriminator for this command ("createMyAddress").
    """

    type: str = "createMyAddress"


@dataclass(kw_only=True)
class DeleteMyAddress:
    """Command to delete the user's address.

    Attributes:
        type: Discriminator for this command ("deleteMyAddress").
    """

    type: str = "deleteMyAddress"


@dataclass(kw_only=True)
class ShowMyAddress:
    """Command to show the user's address.

    Attributes:
        type: Discriminator for this command ("showMyAddress").
    """

    type: str = "showMyAddress"


@dataclass(kw_only=True)
class SetProfileAddress:
    """Command to set whether to include the address in the user's profile.

    Attributes:
        type: Discriminator for this command ("setProfileAddress").
        include_in_profile: Whether to include the address in the profile.
    """

    type: str = "setProfileAddress"
    include_in_profile: bool


@dataclass(kw_only=True)
class AddressAutoAccept:
    """Command to enable or disable auto-accept for addresses.

    Attributes:
        type: Discriminator for this command ("addressAutoAccept").
        auto_accept: Whether to auto-accept addresses.
    """

    type: str = "addressAutoAccept"
    auto_accept: Optional[bool] = None


@dataclass(kw_only=True)
class ReceiveFile:
    """Command to receive a file.

    Attributes:
        type: Discriminator for this command ("receiveFile").
        file_id: The file identifier.
        file_path: Optional path to save the file.
    """

    type: str = "receiveFile"
    file_id: int
    file_path: Optional[str] = None


@dataclass(kw_only=True)
class CancelFile:
    """Command to cancel a file transfer.

    Attributes:
        type: Discriminator for this command ("cancelFile").
        file_id: The file identifier.
    """

    type: str = "cancelFile"
    file_id: int


@dataclass(kw_only=True)
class FileStatus:
    """Command to get the status of a file.

    Attributes:
        type: Discriminator for this command ("fileStatus").
        file_id: The file identifier.
    """

    type: str = "fileStatus"
    file_id: int


@dataclass(kw_only=True)
class APIVerifyContact:
    """Command to verify a contact using a connection code.

    Attributes:
        type: Discriminator for this command ("apiVerifyContact").
        contact_id: The contact identifier.
        connection_code: The connection code to verify.
    """

    type: str = "apiVerifyContact"
    contact_id: int
    connection_code: str


@dataclass(kw_only=True)
class APIVerifyGroupMember:
    """Command to verify a group member using a connection code.

    Attributes:
        type: Discriminator for this command ("apiVerifyGroupMember").
        group_id: The group identifier.
        group_member_id: The group member identifier.
        connection_code: The connection code to verify.
    """

    type: str = "apiVerifyGroupMember"
    group_id: int
    group_member_id: int
    connection_code: str
