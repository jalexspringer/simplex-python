"""
Common test fixtures for domain-specific tests.

These fixtures are shared across all domain test files.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

from simplex_python.client import SimplexClient
from simplex_python.domains.users import UsersClient
from simplex_python.domains.groups import GroupsClient
from simplex_python.domains.chats import ChatsClient
from simplex_python.domains.files import FilesClient


class MockResponse:
    """Mock response object for testing."""

    def __init__(self, type_value, **kwargs):
        self.type = type_value
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def mock_client():
    """Create a mocked SimplexClient with all necessary methods."""
    client = MagicMock(spec=SimplexClient)
    client.send_command = AsyncMock()
    return client


@pytest.fixture
def users_client(mock_client):
    """Create a UsersClient with a mocked SimplexClient."""
    return UsersClient(mock_client)


@pytest.fixture
def chats_client(mock_client):
    """Create a ChatsClient with a mocked SimplexClient."""
    return ChatsClient(mock_client)


@pytest.fixture
def groups_client(mock_client):
    """Create a GroupsClient with a mocked SimplexClient."""
    return GroupsClient(mock_client)


@pytest.fixture
def files_client(mock_client):
    """Create a FilesClient with a mocked SimplexClient."""
    return FilesClient(mock_client)
