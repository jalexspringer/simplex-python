"""
Unit tests for the Users domain client.

Tests the fluent API and functionality of the UsersClient class.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from simplex_python.client_errors import SimplexCommandError
from tests.unit.conftest import MockResponse, mock_client, users_client


class TestUsersClient:
    """Test the functionality of UsersClient."""

    @pytest.mark.asyncio
    async def test_method_chaining(self, users_client, mock_client):
        """Test that methods can be chained together."""
        # Configure mock responses
        mock_client.send_command.side_effect = [
            MockResponse("incognitoUpdated"),
            MockResponse("userContactLinkCreated"),
            MockResponse("userContactLinkUpdated"),
        ]

        # Chain multiple methods with proper awaits
        client = users_client
        client = await client.set_incognito(True)
        client = await client.create_address()
        result = await client.disable_auto_accept()

        # Verify all methods were called in order
        assert mock_client.send_command.call_count == 3
        assert result is users_client  # Should return self

    @pytest.mark.asyncio
    async def test_error_handling(self, users_client, mock_client):
        """Test that error responses are handled correctly."""
        # Configure error response
        mock_client.send_command.return_value = MockResponse(
            "error", error="User not found"
        )

        # Verify error is raised
        with pytest.raises(SimplexCommandError):
            await users_client.set_incognito(True)

    @pytest.mark.asyncio
    async def test_get_active_user(self, users_client, mock_client):
        """Test getting active user with value return."""
        user_data = {"userId": 123, "displayName": "Test User"}
        mock_client.send_command.return_value = MockResponse(
            "activeUser", user=user_data
        )

        # Should return user data, not self
        result = await users_client.get_active()
        assert result == user_data

    @pytest.mark.asyncio
    async def test_create_and_delete_address(self, users_client, mock_client):
        """Test creating and deleting user address."""
        mock_client.send_command.side_effect = [
            MockResponse("userContactLinkCreated", contactLink="simplex://link123"),
            MockResponse("userContactLinkDeleted"),
        ]

        # Properly await each method in the chain
        client = users_client
        client = await client.create_address()
        result = await client.delete_address()

        assert mock_client.send_command.call_count == 2
        assert result is users_client  # Should return self

    @pytest.mark.asyncio
    async def test_set_active_user(self, users_client, mock_client):
        """Test setting active user with and without view password."""
        # Configure mock responses
        mock_client.send_command.side_effect = [
            MockResponse("activeUserSet"),
            MockResponse("activeUserSet"),
        ]

        # Test without view password
        client = users_client
        result = await client.set_active(123)

        # Test with view password
        client = users_client
        result_with_pwd = await client.set_active(456, view_pwd="password123")

        # Verify calls were made with correct parameters
        assert mock_client.send_command.call_count == 2
        # Check that the first call was made without view_pwd
        cmd1 = mock_client.send_command.call_args_list[0][0][0]
        assert cmd1.user_id == 123
        assert cmd1.view_pwd is None
        # Check that the second call included view_pwd
        cmd2 = mock_client.send_command.call_args_list[1][0][0]
        assert cmd2.user_id == 456
        assert cmd2.view_pwd == "password123"

        # Both calls should return self for chaining
        assert result is users_client
        assert result_with_pwd is users_client

    @pytest.mark.asyncio
    async def test_hide_unhide_user(self, users_client, mock_client):
        """Test hiding and unhiding user profiles."""
        # Configure mock responses
        mock_client.send_command.side_effect = [
            MockResponse("userHidden"),
            MockResponse("userUnhidden"),
        ]

        # Test hide_user
        client = users_client
        result_hide = await client.hide_user(123, view_pwd="password123")

        # Test unhide_user
        client = users_client
        result_unhide = await client.unhide_user(123, view_pwd="password123")

        # Verify calls were made with correct parameters
        assert mock_client.send_command.call_count == 2
        # Check hide_user call
        cmd1 = mock_client.send_command.call_args_list[0][0][0]
        assert cmd1.user_id == 123
        assert cmd1.view_pwd == "password123"
        assert cmd1.type == "apiHideUser"
        # Check unhide_user call
        cmd2 = mock_client.send_command.call_args_list[1][0][0]
        assert cmd2.user_id == 123
        assert cmd2.view_pwd == "password123"
        assert cmd2.type == "apiUnhideUser"

        # Both calls should return self for chaining
        assert result_hide is users_client
        assert result_unhide is users_client

    @pytest.mark.asyncio
    async def test_list_users(self, users_client, mock_client):
        """Test listing all users."""
        # Configure mock response
        users_data = [
            {"userId": 123, "displayName": "User 1"},
            {"userId": 456, "displayName": "User 2"},
        ]
        mock_client.send_command.return_value = MockResponse(
            "usersList", users=users_data
        )

        # Call list_users
        result = await users_client.list_users()

        # Verify correct command was sent
        assert mock_client.send_command.call_count == 1
        cmd = mock_client.send_command.call_args[0][0]
        assert cmd.type == "listUsers"

        # Should return users data, not self
        assert result == users_data
