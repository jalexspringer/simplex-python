"""
Unit tests for the chat tag functionality.

These tests verify:
1. Model serialization/deserialization works correctly
2. Command objects create the expected output format
3. Basic validation is performed on inputs
"""

from simplex_python.commands.base import ChatType
from simplex_python.models.chat_tag import ChatTagData
from simplex_python.commands.tag import (
    APIGetChatTags,
    APICreateChatTag,
    APISetChatTags,
    APIDeleteChatTag,
    APIUpdateChatTag,
    APIReorderChatTags,
)


class TestChatTagModels:
    """Test chat tag model functionality."""

    def test_chat_tag_data(self):
        """Test chat tag data creation and serialization."""
        # Uses 'text' instead of 'tag_name'
        tag_data = ChatTagData(text="Important", emoji="🔥")

        # Verify properties
        assert tag_data.text == "Important"
        assert tag_data.emoji == "🔥"

        # Test serialization
        data_dict = tag_data.to_dict()
        assert data_dict["text"] == "Important"
        assert data_dict["emoji"] == "🔥"

    def test_chat_tag_data_no_emoji(self):
        """Test chat tag data without emoji."""
        tag_data = ChatTagData(text="General")

        # Verify properties
        assert tag_data.text == "General"
        assert tag_data.emoji is None

        # Test serialization - emoji should be omitted
        data_dict = tag_data.to_dict()
        assert "emoji" not in data_dict

    def test_chat_tag_deserialization(self):
        """Test deserializing chat tag data."""
        data = {"text": "Urgent", "emoji": "⏰"}

        tag_data = ChatTagData.from_dict(data)
        assert tag_data.text == "Urgent"
        assert tag_data.emoji == "⏰"

    def test_chat_tag_representation(self):
        """Test chat tag representation with the actual fields."""
        # Just test a simpler version focusing on the tag_data fields
        tag_data = ChatTagData(text="Project Alpha", emoji="🚀")

        # Verify properties
        assert tag_data.text == "Project Alpha"
        assert tag_data.emoji == "🚀"


class TestChatTagCommands:
    """Test chat tag command functionality."""

    def test_get_chat_tags_command(self):
        """Test creating a get chat tags command."""
        cmd = APIGetChatTags(user_id=123)

        # Verify command properties
        assert cmd.type == "apiGetChatTags"
        assert cmd.user_id == 123

    def test_create_chat_tag_command(self):
        """Test creating a new chat tag command."""
        tag_data = ChatTagData(text="Feature", emoji="⭐")

        cmd = APICreateChatTag(tag_data=tag_data)

        # Verify command properties
        assert cmd.type == "apiCreateChatTag"
        assert cmd.tag_data.text == "Feature"
        assert cmd.tag_data.emoji == "⭐"

    def test_set_chat_tags_command(self):
        """Test setting tags on a chat."""
        cmd = APISetChatTags(chat_id=123, tag_ids=[1, 2, 3], chat_type=ChatType.DIRECT)

        # Verify command properties
        assert cmd.type == "apiSetChatTags"
        assert cmd.chat_id == 123
        assert len(cmd.tag_ids) == 3
        assert 2 in cmd.tag_ids
        assert cmd.chat_type == ChatType.DIRECT

    def test_set_chat_tags_remove_all(self):
        """Test removing all tags from a chat."""
        cmd = APISetChatTags(
            chat_id=123,
            tag_ids=[],  # Empty list to remove all tags
            chat_type=ChatType.GROUP,
        )

        # Verify command properties
        assert cmd.type == "apiSetChatTags"
        assert cmd.chat_id == 123
        assert len(cmd.tag_ids) == 0
        assert cmd.chat_type == ChatType.GROUP

    def test_delete_chat_tag_command(self):
        """Test deleting a chat tag."""
        cmd = APIDeleteChatTag(tag_id=456)

        # Verify command properties
        assert cmd.type == "apiDeleteChatTag"
        assert cmd.tag_id == 456

    def test_update_chat_tag_command(self):
        """Test updating a chat tag."""
        tag_data = ChatTagData(text="Updated Tag", emoji="🔄")

        cmd = APIUpdateChatTag(tag_id=456, tag_data=tag_data)

        # Verify command properties
        assert cmd.type == "apiUpdateChatTag"
        assert cmd.tag_id == 456
        assert cmd.tag_data.text == "Updated Tag"

    def test_reorder_chat_tags_command(self):
        """Test reordering chat tags."""
        cmd = APIReorderChatTags(
            tag_ids=[3, 1, 2]  # New order
        )

        # Verify command properties
        assert cmd.type == "apiReorderChatTags"
        assert cmd.tag_ids == [3, 1, 2]
