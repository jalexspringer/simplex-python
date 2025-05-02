"""
Reaction commands for Simplex messaging system.

This module defines command classes for message reaction operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseCommand, ChatType
from ..models.reaction import MsgReaction


@dataclass(kw_only=True)
class APIChatItemReaction(BaseCommand):
    """Command to add or remove a reaction to/from a chat item.
    
    Attributes:
        type: Command type identifier ("apiChatItemReaction").
        chat_type: Type of chat (direct, group, etc.).
        chat_id: Chat identifier.
        chat_item_id: Chat item identifier.
        add: Whether to add (True) or remove (False) the reaction.
        reaction: The reaction to add or remove.
    """
    
    type: str = "apiChatItemReaction"
    chat_type: ChatType
    chat_id: int
    chat_item_id: int
    add: bool
    reaction: MsgReaction


@dataclass(kw_only=True)
class APIGetReactionMembers(BaseCommand):
    """Command to get members who reacted to a group message.
    
    Attributes:
        type: Command type identifier ("apiGetReactionMembers").
        user_id: User identifier.
        group_id: Group identifier.
        chat_item_id: Chat item identifier.
        reaction: The reaction to get members for.
    """
    
    type: str = "apiGetReactionMembers"
    user_id: int
    group_id: int
    chat_item_id: int
    reaction: MsgReaction
