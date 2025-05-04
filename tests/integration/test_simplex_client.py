"""
Integration tests for the SimpleX Chat Python client.

These tests run against a live SimpleX Chat server and verify that
commands and responses are working correctly.
"""

import asyncio
import logging
import os
import pytest
import tempfile
import pprint

from simplex_python.client import SimplexClient
from simplex_python.commands.base import ServerProtocol
from simplex_python.transport import ChatServer
from simplex_python.client_errors import SimplexClientError, SimplexCommandError
from simplex_python.commands import ListUsers


# Test configuration
TEST_SERVER = os.environ.get("SIMPLEX_TEST_SERVER", "localhost")
TEST_PORT = int(os.environ.get("SIMPLEX_TEST_PORT", "5225"))
TEST_TIMEOUT = 5  # Seconds

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("simplex_test")


@pytest.fixture
async def client():
    """Create and connect a SimplexClient for testing."""
    server = ChatServer(host=TEST_SERVER, port=str(TEST_PORT))
    async with SimplexClient(server, timeout=TEST_TIMEOUT) as client:
        yield client
