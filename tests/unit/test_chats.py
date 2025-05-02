"""
Unit tests for the Chats domain client.

Tests the fluent API and functionality of the ChatsClient class.
"""

import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tests.unit.conftest import MockResponse


class TestChatsClient:
    """Test the functionality of ChatsClient."""

    @pytest.mark.asyncio
    async def test_send_message_chain(self, chats_client, mock_client):
        """Test sending messages with chaining."""
        mock_client.send_command.side_effect = [
            MockResponse("newChatItems"),
            MockResponse("newChatItems"),
        ]

        # Properly await each method in the chain
        client = chats_client
        client = await client.send_message(123, "Hello")
        result = await client.send_message(456, "World")

        assert mock_client.send_command.call_count == 2
        assert result is chats_client  # Should return self

    @pytest.mark.asyncio
    async def test_get_chats(self, chats_client, mock_client):
        """Test getting chats with value return."""
        chats_data = [{"chatId": 1}, {"chatId": 2}]
        mock_client.send_command.return_value = MockResponse(
            "apiChats", chats=chats_data
        )

        # Should return chats data, not self
        result = await chats_client.get_chats(123)
        assert result == chats_data

    @pytest.mark.asyncio
    async def test_chat_operations_chain(self, chats_client, mock_client):
        """Test complex chat operations with chaining."""
        mock_client.send_command.side_effect = [
            MockResponse("newChatItems"),
            MockResponse("chatItemUpdated"),
            MockResponse("chatItemDeleted"),
            MockResponse("chatCleared"),
        ]

        # Properly await each method in the chain
        client = chats_client
        client = await client.send_message(123, "Hello")
        client = await client.update_chat_item(123, 456, "Updated")
        client = await client.delete_chat_item(123, 456)
        result = await client.clear_chat(123)

        assert mock_client.send_command.call_count == 4
        assert result is chats_client  # Should return self
