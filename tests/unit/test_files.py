"""
Unit tests for the Files domain client.

Tests the fluent API and functionality of the FilesClient class.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from pathlib import Path

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from simplex_python.errors import SimplexCommandError
from tests.unit.conftest import MockResponse, mock_client, files_client


class TestFilesClient:
    """Test the functionality of FilesClient."""

    @pytest.mark.asyncio
    async def test_file_operations_chain(self, files_client, mock_client):
        """Test file operations with chaining."""
        # Patch Path.exists to always return True to avoid FileNotFoundError
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.is_dir", return_value=True),
            patch("pathlib.Path.absolute", return_value=Path("/tmp/test.txt")),
            patch("pathlib.Path.mkdir"),
        ):
            mock_client.send_command.side_effect = [
                MockResponse("newChatItems"),
                MockResponse("fileReceived"),
            ]

            # Properly await each method in the chain
            client = files_client
            # Use send instead of accept_file
            client = await client.send(123, "/tmp/test.txt")
            # Use receive instead
            result = await client.receive(456, "/tmp/downloaded.txt")

            assert mock_client.send_command.call_count == 2
            assert result is files_client  # Should return self

    @pytest.mark.asyncio
    async def test_file_status_value_return(self, files_client, mock_client):
        """Test getting file status with value return."""
        file_data = {"fileId": 123, "status": "rcvAccepted"}
        mock_client.send_command.return_value = MockResponse(
            "fileStatusUpdated", fileTransfer=file_data
        )

        # Use status instead of get_status
        result = await files_client.status(123)
        assert result == file_data

    @pytest.mark.asyncio
    async def test_file_not_found_error(self, files_client, mock_client):
        """Test file not found error handling."""
        # Configure error response for file not found
        mock_client.send_command.return_value = MockResponse(
            "error", error={"type": "fileNotFound"}
        )

        # Verify error is raised, use status instead of get_status
        with pytest.raises(SimplexCommandError):
            await files_client.status(999)

    @pytest.mark.asyncio
    async def test_cancel_file_transfer(self, files_client, mock_client):
        """Test cancelling a file transfer."""
        mock_client.send_command.return_value = MockResponse("fileCancelled")

        result = await files_client.cancel(123)

        # Verify correct command was sent
        assert mock_client.send_command.call_count == 1
        args = mock_client.send_command.call_args[0][0]
        assert args["type"] == "cancelFile"
        assert args["file_id"] == 123

        # Should return self for chaining
        assert result is files_client

    @pytest.mark.asyncio
    async def test_set_temp_folder(self, files_client, mock_client):
        """Test setting temporary folder for file downloads."""
        # Patch directory checks
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.is_dir", return_value=True),
            patch("pathlib.Path.mkdir"),
        ):
            mock_client.send_command.return_value = MockResponse("tempFolderSet")

            result = await files_client.set_temp_folder("/tmp/downloads")

            # Should return self for chaining
            assert result is files_client
