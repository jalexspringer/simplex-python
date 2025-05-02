"""
Chat and messaging commands for Simplex messaging system.

This module defines command classes for chat-related operations:
- Creating and managing chats
- Sending and managing messages
- Reading and clearing chats
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from .base import BaseCommand, ChatType, DeleteMode
from ..models.message import ComposedMessage, MsgContent
from ..models.pagination import ChatPagination, ItemRange
from ..models.archive import ArchiveConfig


@dataclass(kw_only=True)
class StartChat(BaseCommand):
    """Command to start the chat system.

    Attributes:
        type: Command type identifier ("startChat").
        subscribe_connections: Whether to subscribe to connection events.
        enable_expire_chat_items: Whether to enable chat item expiration.
        start_xftp_workers: Whether to start XFTP workers.
    """

    type: str = "startChat"
    subscribe_connections: Optional[bool] = None
    enable_expire_chat_items: Optional[bool] = None
    start_xftp_workers: Optional[bool] = None


@dataclass(kw_only=True)
class APIStopChat(BaseCommand):
    """Command to stop the chat system.

    Attributes:
        type: Command type identifier ("apiStopChat").
    """

    type: str = "apiStopChat"


@dataclass(kw_only=True)
class SetTempFolder(BaseCommand):
    """Command to set the temporary folder path.

    Attributes:
        type: Command type identifier ("setTempFolder").
        temp_folder: Path to temporary folder.
    """

    type: str = "setTempFolder"
    temp_folder: str


@dataclass(kw_only=True)
class SetFilesFolder(BaseCommand):
    """Command to set the files folder path.

    Attributes:
        type: Command type identifier ("setFilesFolder").
        file_path: Path to files folder.
    """

    type: str = "setFilesFolder"
    file_path: str


@dataclass(kw_only=True)
class APIExportArchive(BaseCommand):
    """Command to export chat archive.

    Attributes:
        type: Command type identifier ("apiExportArchive").
        config: Archive configuration.
    """

    type: str = "apiExportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIImportArchive(BaseCommand):
    """Command to import chat archive.

    Attributes:
        type: Command type identifier ("apiImportArchive").
        config: Archive configuration.
    """

    type: str = "apiImportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIDeleteStorage(BaseCommand):
    """Command to delete chat storage.

    Attributes:
        type: Command type identifier ("apiDeleteStorage").
    """

    type: str = "apiDeleteStorage"


@dataclass(kw_only=True)
class APIGetChats(BaseCommand):
    """Command to get all chats for a user.

    Attributes:
        type: Command type identifier ("apiGetChats").
        user_id: User identifier.
        pending_connections: Whether to include pending connections.
    """

    type: str = "apiGetChats"
    user_id: int
    pending_connections: Optional[bool] = None


@dataclass(kw_only=True)
class APIGetChat(BaseCommand):
    """Command to get a specific chat.

    Attributes:
        type: Command type identifier ("apiGetChat").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        pagination: Pagination parameters.
        search: Optional search query.
    """

    type: str = "apiGetChat"
    chat_type: ChatType
    chat_id: int
    pagination: ChatPagination
    search: Optional[str] = None


@dataclass(kw_only=True)
class APISendMessage(BaseCommand):
    """Command to send messages to a chat.

    Attributes:
        type: Command type identifier ("apiSendMessage").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        messages: List of messages to send.
    """

    type: str = "apiSendMessage"
    chat_type: ChatType
    chat_id: int
    messages: List[ComposedMessage]


@dataclass(kw_only=True)
class APIUpdateChatItem(BaseCommand):
    """Command to update a chat item.

    Attributes:
        type: Command type identifier ("apiUpdateChatItem").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        chat_item_id: Chat item identifier.
        msg_content: New message content.
    """

    type: str = "apiUpdateChatItem"
    chat_type: ChatType
    chat_id: int
    chat_item_id: int
    msg_content: MsgContent


@dataclass(kw_only=True)
class APIDeleteChatItem(BaseCommand):
    """Command to delete a chat item.

    Attributes:
        type: Command type identifier ("apiDeleteChatItem").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        chat_item_id: Chat item identifier.
        delete_mode: Deletion mode.
    """

    type: str = "apiDeleteChatItem"
    chat_type: ChatType
    chat_id: int
    chat_item_id: int
    delete_mode: DeleteMode


@dataclass(kw_only=True)
class APIDeleteMemberChatItem(BaseCommand):
    """Command to delete a group member's chat item.

    Attributes:
        type: Command type identifier ("apiDeleteMemberChatItem").
        group_id: Group identifier.
        group_member_id: Group member identifier.
        item_id: Item identifier.
    """

    type: str = "apiDeleteMemberChatItem"
    group_id: int
    group_member_id: int
    item_id: int


@dataclass(kw_only=True)
class APIChatRead(BaseCommand):
    """Command to mark chat items as read.

    Attributes:
        type: Command type identifier ("apiChatRead").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        item_range: Optional range of items to mark as read.
    """

    type: str = "apiChatRead"
    chat_type: ChatType
    chat_id: int
    item_range: Optional[ItemRange] = None


@dataclass(kw_only=True)
class APIDeleteChat(BaseCommand):
    """Command to delete a chat.

    Attributes:
        type: Command type identifier ("apiDeleteChat").
        chat_type: Type of chat.
        chat_id: Chat identifier.
    """

    type: str = "apiDeleteChat"
    chat_type: ChatType
    chat_id: int


@dataclass(kw_only=True)
class APIClearChat(BaseCommand):
    """Command to clear all messages from a chat.

    Attributes:
        type: Command type identifier ("apiClearChat").
        chat_type: Type of chat.
        chat_id: Chat identifier.
    """

    type: str = "apiClearChat"
    chat_type: ChatType
    chat_id: int


@dataclass(kw_only=True)
class APIAcceptContact(BaseCommand):
    """Command to accept a contact request.

    Attributes:
        type: Command type identifier ("apiAcceptContact").
        contact_req_id: Contact request identifier.
    """

    type: str = "apiAcceptContact"
    contact_req_id: int


@dataclass(kw_only=True)
class APIRejectContact(BaseCommand):
    """Command to reject a contact request.

    Attributes:
        type: Command type identifier ("apiRejectContact").
        contact_req_id: Contact request identifier.
    """

    type: str = "apiRejectContact"
    contact_req_id: int


@dataclass(kw_only=True)
class APISetContactAlias(BaseCommand):
    """Command to set a contact's local alias.

    Attributes:
        type: Command type identifier ("apiSetContactAlias").
        contact_id: Contact identifier.
        local_alias: Local alias to set.
    """

    type: str = "apiSetContactAlias"
    contact_id: int
    local_alias: str
