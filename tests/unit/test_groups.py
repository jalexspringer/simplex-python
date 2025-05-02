"""
Unit tests for the Groups domain client.

Tests the fluent API and functionality of the GroupsClient class.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from simplex_python.errors import SimplexCommandError
from tests.unit.conftest import MockResponse, mock_client, groups_client


class TestGroupsClient:
    """Test the functionality of GroupsClient."""

    @pytest.mark.asyncio
    async def test_group_management_chain(self, groups_client, mock_client):
        """Test group management operations with chaining."""
        mock_client.send_command.side_effect = [
            MockResponse("groupCreated"),
            MockResponse("memberAdded"),
            MockResponse("groupProfileUpdated"),
        ]

        # Properly await each method in the chain
        client = groups_client
        client = await client.create("Test Group")
        client = await client.add_member(123, 456)
        result = await client.update_profile(123, "Updated Group")

        assert mock_client.send_command.call_count == 3
        assert result is groups_client  # Should return self

    @pytest.mark.asyncio
    async def test_create_link_value_return(self, groups_client, mock_client):
        """Test creating a group link with value return."""
        link_data = "simplex://?v=1&smp=smp%3A%2F%2Fu2dS9sG8nMNURyZRZw6Ucs"
        mock_client.send_command.return_value = MockResponse(
            "groupLinkCreated", groupLink=link_data
        )

        # Should return link data, not self
        result = await groups_client.create_link(123)
        assert result == link_data
