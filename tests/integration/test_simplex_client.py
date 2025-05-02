"""
Integration test for SimplexClient.

Tests basic functionality like connecting to a server and retrieving the active user.
"""

import logging
import os
import pytest
from typing import AsyncGenerator

from simplex_python.client import SimplexClient


# Test configuration from environment with sensible defaults
TEST_SERVER = os.environ.get("SIMPLEX_TEST_SERVER", "localhost")
TEST_PORT = int(os.environ.get("SIMPLEX_TEST_PORT", "5225"))
TEST_TIMEOUT = float(os.environ.get("SIMPLEX_TEST_TIMEOUT", "5.0"))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def simplex_server_url() -> str:
    """Return the server URL for tests."""
    return f"ws://{TEST_SERVER}:{TEST_PORT}"


@pytest.fixture
async def simplex_client(
    simplex_server_url: str,
) -> AsyncGenerator[SimplexClient, None]:
    """Create a SimplexClient connected to the test server."""
    logger.info(f"Connecting to SimpleX server at {simplex_server_url}")

    client = SimplexClient(simplex_server_url, timeout=TEST_TIMEOUT)
    try:
        await client.connect()
        yield client
    finally:
        await client.disconnect()


@pytest.mark.asyncio
async def test_client_connect_and_get_active_user(
    simplex_client: SimplexClient,
) -> None:
    """Test that we can connect to the server and get the active user."""
    # Verify the client is connected
    assert simplex_client.connected, "Client should be connected"

    # Get the active user
    user = await simplex_client.users.get_active()

    # Log the user info for debugging
    logger.info(f"Active user: {user}")

    # We should have a user object with at least a profile
    assert user is not None, "Should have an active user"
    assert "profile" in user, "User should have a profile"
    assert "displayName" in user["profile"], "User profile should have a displayName"

    # Just informational - print the display name
    logger.info(f"Active user display name: {user['profile']['displayName']}")
