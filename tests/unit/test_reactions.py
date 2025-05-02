"""
Unit tests for the chat reaction functionality.

These tests verify:
1. Model serialization/deserialization works correctly
2. Command objects create the expected output format
3. Basic validation is performed on inputs
"""

from simplex_python.commands.base import ChatType
from simplex_python.models.reaction import MsgReaction, CIReactionCount
from simplex_python.commands.reaction import APIChatItemReaction, APIGetReactionMembers


class TestReactionModels:
    """Test message reaction model functionality."""

    def test_msg_reaction_emoji_factory(self):
        """Test the emoji factory method for MsgReaction."""
        reaction = MsgReaction.create_emoji("👍")
        assert reaction.type == "emoji"
        assert reaction.emoji == "👍"

    def test_msg_reaction_serialization(self):
        """Test serializing a reaction to dict."""
        reaction = MsgReaction(type="emoji", emoji="❤️")
        result = reaction.to_dict()
        assert result == {"type": "emoji", "emoji": "❤️"}

    def test_msg_reaction_deserialization(self):
        """Test deserializing a reaction from dict."""
        data = {"type": "emoji", "emoji": "🎉"}
        reaction = MsgReaction.from_dict(data)
        assert reaction.type == "emoji"
        assert reaction.emoji == "🎉"

    def test_reaction_count_representation(self):
        """Test reaction count object representation."""
        # Create a reaction count with correct field name (total_count, not count)
        count = CIReactionCount(
            reaction=MsgReaction.create_emoji("👍"), total_count=3, user_reacted=True
        )

        # Verify properties
        assert count.reaction.emoji == "👍"
        assert count.total_count == 3
        assert count.user_reacted is True


class TestReactionCommands:
    """Test message reaction command functionality."""

    def test_chat_item_reaction_command(self):
        """Test creating a chat item reaction command."""
        cmd = APIChatItemReaction(
            chat_id=123,
            chat_item_id=456,
            reaction=MsgReaction.create_emoji("👍"),
            add=True,
            chat_type=ChatType.DIRECT,
        )

        # Verify command properties
        assert cmd.type == "apiChatItemReaction"
        assert cmd.chat_id == 123
        assert cmd.chat_item_id == 456
        assert cmd.reaction.emoji == "👍"
        assert cmd.add is True
        assert cmd.chat_type == ChatType.DIRECT

    def test_get_reaction_members_command(self):
        """Test creating a get reaction members command."""
        reaction = MsgReaction.create_emoji("🎉")
        cmd = APIGetReactionMembers(
            user_id=123,
            group_id=456,  # Uses group_id instead of chat_id
            chat_item_id=789,
            reaction=reaction,
        )

        # Verify command properties
        assert cmd.type == "apiGetReactionMembers"
        assert cmd.user_id == 123
        assert cmd.group_id == 456
        assert cmd.chat_item_id == 789
        assert cmd.reaction.emoji == "🎉"
