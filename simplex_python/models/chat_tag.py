"""
Chat tag models for the Simplex messaging system.

This module defines data structures for chat tags, which allow users
to categorize and organize their chats using custom labels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ChatTagData:
    """Data for creating or updating a chat tag.
    
    Attributes:
        text: The text label for the tag.
        emoji: Optional emoji to associate with the tag.
    """
    text: str
    emoji: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the chat tag data to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the chat tag data.
        """
        result = {"text": self.text}
        if self.emoji is not None:
            result["emoji"] = self.emoji
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChatTagData:
        """Create a ChatTagData instance from a dictionary.
        
        Args:
            data: Dictionary containing chat tag data.
            
        Returns:
            A ChatTagData instance.
        """
        return cls(
            text=data.get("text", ""),
            emoji=data.get("emoji")
        )


@dataclass
class ChatTag:
    """A chat tag that can be applied to chats for organization.
    
    Attributes:
        tag_id: Unique identifier for the tag.
        user_id: ID of the user who owns this tag.
        text: The text label for the tag.
        emoji: Optional emoji to associate with the tag.
        order: Display order of the tag in the list of tags.
    """
    tag_id: int
    user_id: int
    text: str
    order: int
    emoji: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the chat tag to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the chat tag.
        """
        result = {
            "tagId": self.tag_id,
            "userId": self.user_id,
            "text": self.text,
            "order": self.order
        }
        if self.emoji is not None:
            result["emoji"] = self.emoji
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChatTag:
        """Create a ChatTag instance from a dictionary.
        
        Args:
            data: Dictionary containing chat tag data.
            
        Returns:
            A ChatTag instance.
        """
        return cls(
            tag_id=data.get("tagId", 0),
            user_id=data.get("userId", 0),
            text=data.get("text", ""),
            emoji=data.get("emoji"),
            order=data.get("order", 0)
        )
