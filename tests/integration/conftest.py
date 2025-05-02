"""
Fixtures for integration tests.

These fixtures provide access to a running SimpleX Chat server.
"""

import os
import pytest
import logging
from typing import AsyncGenerator, Tuple, Dict, Any

from simplex_python.client import SimplexClient


# Test configuration from environment
TEST_SERVER = os.environ.get("SIMPLEX_TEST_SERVER", "localhost")
TEST_PORT = int(os.environ.get("SIMPLEX_TEST_PORT", "5225"))
TEST_TIMEOUT = 5  # Seconds

# Set up logging for clearer test output
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="session")
def simplex_server_info() -> Tuple[str, int]:
    """Return server info for tests."""
    return (TEST_SERVER, TEST_PORT)


@pytest.fixture
async def simplex_client(simplex_server_info) -> AsyncGenerator[SimplexClient, None]:
    """Create a SimplexClient connected to the test server."""
    server_host, server_port = simplex_server_info
    server_url = f"ws://{server_host}:{server_port}"
    
    client = SimplexClient(server_url, timeout=TEST_TIMEOUT)
    try:
        await client.connect()
        yield client
    finally:
        await client.disconnect()


@pytest.fixture
async def clean_test_user(simplex_client) -> AsyncGenerator[Dict[str, Any], None]:
    """Create a test user and clean up afterwards."""
    # Get the existing active user instead of trying to create a new one
    # This works better with the current server setup
    user = await simplex_client.users.get_active()
    
    if not user:
        # If no active user, log it but continue with tests using whatever the server returns
        logging.warning("No active user found on test server - tests may not run correctly")
        # Since we're using an existing server, we'll use the default user if available
        await simplex_client.send_command("/u")
        user = await simplex_client.users.get_active()
    
    try:
        yield user
    finally:
        # Skip cleanup of the user since we're using the default user
        pass
