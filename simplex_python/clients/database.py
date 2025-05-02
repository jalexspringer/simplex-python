"""
Database domain client for SimplexClient.

Provides a fluent API for database-related operations.
"""

import logging
import os
from typing import Optional, TYPE_CHECKING
from ..commands import (
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
    ArchiveConfig,
)
from ..response import ChatResponse
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class DatabaseClient:
    """
    Client for database-related operations in SimplexClient.

    This client is accessed via the `database` property of SimplexClient
    and provides methods for managing database operations, such as
    exporting and importing archives and managing storage data.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def export_archive(
        self,
        archive_path: str,
        disable_compression: bool = False,
        parent_temp_directory: Optional[str] = None,
    ) -> ChatResponse:
        """
        Export a database archive.

        Args:
            archive_path: Path where the archive will be saved.
            disable_compression: Whether to disable compression of the archive.
            parent_temp_directory: Optional parent directory for temporary files.

        Returns:
            ChatResponse containing the result of the export operation.
        """
        # Ensure the parent directory exists
        parent_dir = os.path.dirname(archive_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            logger.info(f"Created parent directory for archive: {parent_dir}")

        # Create archive configuration
        config = ArchiveConfig(
            archivePath=archive_path,
            disableCompression=disable_compression,
            parentTempDirectory=parent_temp_directory,
        )

        cmd = APIExportArchive(
            type="apiExportArchive",
            config=config,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to export archive: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "archiveExported" or similar
        expected_types = ["archiveExported"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to export archive: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def import_archive(
        self,
        archive_path: str,
        disable_compression: bool = False,
        parent_temp_directory: Optional[str] = None,
    ) -> ChatResponse:
        """
        Import a database archive.

        Args:
            archive_path: Path to the archive file to import.
            disable_compression: Whether the archive is uncompressed.
            parent_temp_directory: Optional parent directory for temporary files.

        Returns:
            ChatResponse containing the result of the import operation.
        """
        # Verify the archive file exists
        if not os.path.exists(archive_path):
            error_msg = f"Archive file not found: {archive_path}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, None)

        # Create archive configuration
        config = ArchiveConfig(
            archivePath=archive_path,
            disableCompression=disable_compression,
            parentTempDirectory=parent_temp_directory,
        )

        cmd = APIImportArchive(
            type="apiImportArchive",
            config=config,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to import archive: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "archiveImported" or similar
        expected_types = ["archiveImported"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to import archive: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def delete_storage(self) -> ChatResponse:
        """
        Delete all storage data.

        This is a destructive operation that will delete all database content.
        Use with caution.

        Returns:
            ChatResponse containing the result of the delete operation.
        """
        cmd = APIDeleteStorage(
            type="apiDeleteStorage",
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to delete storage: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "storageDeleted" or similar
        expected_types = ["storageDeleted"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to delete storage: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp
