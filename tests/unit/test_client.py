"""
Unit tests for the core SimplexClient functionality.

Tests client initialization, connection, command sending, and domain client access.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from simplex_python.client import SimplexClient
from simplex_python.domains.users import UsersClient
from simplex_python.domains.groups import GroupsClient
from simplex_python.domains.chats import ChatsClient
from simplex_python.domains.files import FilesClient


class TestSimplexClient:
    """Test the core functionality of SimplexClient."""

    def test_domain_client_properties(self):
        """Test that domain client properties return correct instances."""
        client = SimplexClient("ws://localhost:5225")

        # Test domain clients are created and returned
        assert isinstance(client.users, UsersClient)
        assert isinstance(client.groups, GroupsClient)
        assert isinstance(client.chats, ChatsClient)
        assert isinstance(client.files, FilesClient)

        # Test domain clients are cached
        users_client1 = client.users
        users_client2 = client.users
        assert users_client1 is users_client2

    @pytest.mark.asyncio
    async def test_client_connection(self):
        """Test client connection and disconnection."""
        with patch("simplex_python.transport.ChatTransport.connect") as mock_connect:
            mock_transport = MagicMock()
            mock_transport.close = AsyncMock()
            mock_connect.return_value = mock_transport

            client = SimplexClient("ws://localhost:5225")
            await client.connect()

            # Assert connect was called
            mock_connect.assert_called_once()
            assert client.connected is True

            # Test disconnection
            await client.disconnect()
            mock_transport.close.assert_called_once()
            assert client.connected is False

    @pytest.mark.asyncio
    async def test_cross_domain_access(self):
        """Test cross-domain access and method chaining between domains."""
        with patch(
            "simplex_python.client.SimplexClient.send_command", new_callable=AsyncMock
        ) as mock_send:
            # Setup mock client
            client = SimplexClient("ws://localhost:5225")
            client._connected = True  # Mock connection state

            # Test cross-domain access
            users = client.users
            chats = users._client.chats
            groups = chats._client.groups

            # Ensure all domains reference the same client
            assert users._client is client
            assert chats._client is client
            assert groups._client is client
