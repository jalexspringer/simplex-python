"""
Files domain client for SimplexClient.

Provides a fluent API for file-related operations.
"""

import logging
import os
from typing import Optional, TYPE_CHECKING
from ..commands import (
    SetTempFolder,
    SetFilesFolder,
    ReceiveFile,
    CancelFile,
    FileStatus,
)
from ..response import ChatResponse
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class FilesClient:
    """
    Client for file-related operations in SimplexClient.

    This client is accessed via the `files` property of SimplexClient
    and provides methods for managing file transfers and storage locations.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def set_temp_folder(self, temp_folder: str) -> ChatResponse:
        """
        Set the temporary folder for file operations.

        Args:
            temp_folder: Path to the temporary folder.

        Returns:
            ChatResponse containing the result of the operation.
        """
        # Ensure the folder exists
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder, exist_ok=True)
            logger.info(f"Created temporary folder: {temp_folder}")

        cmd = SetTempFolder(
            type="setTempFolder",
            tempFolder=temp_folder,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to set temp folder: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def set_files_folder(self, files_folder: str) -> ChatResponse:
        """
        Set the folder for file storage.

        Args:
            files_folder: Path to the files folder.

        Returns:
            ChatResponse containing the result of the operation.
        """
        # Ensure the folder exists
        if not os.path.exists(files_folder):
            os.makedirs(files_folder, exist_ok=True)
            logger.info(f"Created files folder: {files_folder}")

        cmd = SetFilesFolder(
            type="setFilesFolder",
            filePath=files_folder,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to set files folder: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def receive_file(
        self, file_id: int, file_path: Optional[str] = None
    ) -> ChatResponse:
        """
        Receive a file transfer.

        Args:
            file_id: ID of the file to receive.
            file_path: Optional custom path to save the file.

        Returns:
            ChatResponse containing the result of the file receive operation.
        """
        cmd = ReceiveFile(
            type="receiveFile",
            fileId=file_id,
            filePath=file_path,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to receive file: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "fileReceived" or similar, should be verified
        expected_types = ["fileReceived", "fileReceiving"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to receive file: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def cancel_file(self, file_id: int) -> ChatResponse:
        """
        Cancel a file transfer.

        Args:
            file_id: ID of the file transfer to cancel.

        Returns:
            ChatResponse containing the result of the cancel operation.
        """
        cmd = CancelFile(
            type="cancelFile",
            fileId=file_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to cancel file: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "fileCancelled" or similar, should be verified
        expected_types = ["fileCancelled"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to cancel file: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_status(self, file_id: int) -> ChatResponse:
        """
        Get the status of a file transfer.

        Args:
            file_id: ID of the file transfer to check.

        Returns:
            ChatResponse containing the file status information.
        """
        cmd = FileStatus(
            type="fileStatus",
            fileId=file_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get file status: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "fileStatusResult" or similar, should be verified
        expected_types = ["fileStatusResult", "fileStatus"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to get file status: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp
