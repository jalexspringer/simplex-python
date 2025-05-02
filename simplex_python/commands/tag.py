"""
Chat tag commands for Simplex messaging system.

This module defines command classes for chat tag operations:
- Creating, updating, and deleting tags
- Associating tags with chats
- Reordering tags
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from .base import BaseCommand, ChatType
from ..models.chat_tag import ChatTagData


@dataclass(kw_only=True)
class APIGetChatTags(BaseCommand):
    """Command to get all chat tags for a user.

    Attributes:
        type: Command type identifier ("apiGetChatTags").
        user_id: User identifier.
    """

    type: str = "apiGetChatTags"
    user_id: int


@dataclass(kw_only=True)
class APICreateChatTag(BaseCommand):
    """Command to create a new chat tag.

    Attributes:
        type: Command type identifier ("apiCreateChatTag").
        tag_data: Chat tag data containing text and optional emoji.
    """

    type: str = "apiCreateChatTag"
    tag_data: ChatTagData


@dataclass(kw_only=True)
class APISetChatTags(BaseCommand):
    """Command to set tags for a chat.

    Attributes:
        type: Command type identifier ("apiSetChatTags").
        chat_type: Type of chat.
        chat_id: Chat identifier.
        tag_ids: List of tag identifiers to associate with the chat.
                 If None, removes all tags from the chat.
    """

    type: str = "apiSetChatTags"
    chat_type: ChatType
    chat_id: int
    tag_ids: Optional[List[int]] = None


@dataclass(kw_only=True)
class APIDeleteChatTag(BaseCommand):
    """Command to delete a chat tag.

    Attributes:
        type: Command type identifier ("apiDeleteChatTag").
        tag_id: Tag identifier to delete.
    """

    type: str = "apiDeleteChatTag"
    tag_id: int


@dataclass(kw_only=True)
class APIUpdateChatTag(BaseCommand):
    """Command to update a chat tag.

    Attributes:
        type: Command type identifier ("apiUpdateChatTag").
        tag_id: Tag identifier to update.
        tag_data: Updated chat tag data.
    """

    type: str = "apiUpdateChatTag"
    tag_id: int
    tag_data: ChatTagData


@dataclass(kw_only=True)
class APIReorderChatTags(BaseCommand):
    """Command to reorder chat tags.

    Attributes:
        type: Command type identifier ("apiReorderChatTags").
        tag_ids: Ordered list of tag identifiers in the desired display order.
    """

    type: str = "apiReorderChatTags"
    tag_ids: List[int]
