"""
Message handling command classes for the Simplex messaging system.

This module defines the commands for working with messages, including:
- Sending new messages
- Updating existing messages
- Deleting messages
- Managing message content types

All commands inherit from BaseCommand and provide a consistent interface
for message-related operations in the Simplex system.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Union
from .base import BaseCommand, ChatType, ChatItemId, DeleteMode, MsgContent, LinkPreview


@dataclass
class ComposedMessage:
    """A message composed for sending."""

    msgContent: MsgContent
    filePath: Optional[str] = None
    quotedItemId: Optional[ChatItemId] = None


@dataclass(kw_only=True)
class APISendMessage(BaseCommand):
    """Command to send a message via API."""

    type: str = "apiSendMessage"
    chatType: ChatType
    chatId: int
    messages: List[ComposedMessage]


@dataclass(kw_only=True)
class APIUpdateChatItem(BaseCommand):
    """Command to update a chat item via API."""

    type: str = "apiUpdateChatItem"
    chatType: ChatType
    chatId: int
    chatItemId: ChatItemId
    msgContent: MsgContent


@dataclass(kw_only=True)
class APIDeleteChatItem(BaseCommand):
    """Command to delete a chat item via API."""

    type: str = "apiDeleteChatItem"
    chatType: ChatType
    chatId: int
    chatItemId: ChatItemId
    deleteMode: DeleteMode


@dataclass(kw_only=True)
class APIDeleteMemberChatItem(BaseCommand):
    """Command to delete a member's chat item via API."""

    type: str = "apiDeleteMemberChatItem"
    groupId: int
    groupMemberId: int
    itemId: int


# Type alias for MessageCommand
MessageCommand = Union[
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
]
