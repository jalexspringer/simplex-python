"""
Message reaction models for the Simplex messaging system.

This module defines the data structures for message reactions,
which allow users to react to chat messages with emojis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class MsgReaction:
    """Base class for message reactions.
    
    This represents a reaction to a message, with support for 
    emoji reactions and future reaction types through extensibility.
    """
    type: str = "emoji"
    # Adding explicit emoji field to fix attribute access and init
    emoji: Optional[str] = None
    
    @staticmethod
    def create_emoji(emoji_char: str) -> MsgReaction:
        """Create an emoji reaction.
        
        Args:
            emoji_char: The emoji character to use as a reaction
            
        Returns:
            A MsgReaction instance with the specified emoji
        """
        return MsgReaction(type="emoji", emoji=emoji_char)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the reaction to a dictionary for serialization.
        
        Returns:
            A dictionary representation of the reaction
        """
        return {
            "type": self.type,
            self.type: getattr(self, self.type, None)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MsgReaction:
        """Create a reaction instance from a dictionary.
        
        Args:
            data: Dictionary containing reaction data
            
        Returns:
            A MsgReaction instance
        """
        reaction_type = data.get("type", "emoji")
        if reaction_type == "emoji":
            return cls(type=reaction_type, emoji=data.get("emoji"))
        else:
            # Handle unknown reaction types for future extensibility
            return cls(type=reaction_type)


@dataclass
class CIReactionCount:
    """Information about reactions on a chat item.
    
    Attributes:
        reaction: The reaction type
        user_reacted: Whether the current user has added this reaction
        total_count: The total number of users who added this reaction
    """
    reaction: MsgReaction
    user_reacted: bool
    total_count: int
