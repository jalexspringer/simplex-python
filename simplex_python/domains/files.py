"""
Files domain client for the Simplex Chat protocol.
"""

from typing import Any, TypedDict
from pathlib import Path
import logging

from .base import BaseDomainClient
from ..enums import ChatType

logger = logging.getLogger(__name__)


class FileTransfer(TypedDict, total=False):
    """Type definition for file transfer data."""
    
    file_id: int
    file_name: str
    file_path: str
    file_size: int
    file_status: str
    progress: int


class FilesClient(BaseDomainClient["FilesClient"]):
    """Client for file-related operations."""
    
    async def send(self, chat_id: int, file_path: str, chat_type: str | ChatType = "direct") -> "FilesClient":
        """
        Send a file to a chat.
        
        Args:
            chat_id: ID of the chat
            file_path: Path to the file to send
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If sending the file fails
            FileNotFoundError: If the specified file doesn't exist
        """
        logger.debug(f"Sending file {file_path} to chat {chat_id}")
        # Verify file exists
        file = Path(file_path)
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        resp = await self._client.send_command({
            "type": "apiSendMessage",
            "chat_type": chat_type_value,
            "chat_id": chat_id,
            "messages": [{
                "msg_content": {
                    "type": "file",
                    "file_path": str(file.absolute())
                }
            }]
        })
        
        await self._process_response(
            resp,
            "newChatItems",
            f"Failed to send file to chat {chat_id}"
        )
        
        return self
    
    async def receive(self, file_id: int, destination_path: str) -> "FilesClient":
        """
        Download a received file.
        
        Args:
            file_id: ID of the file to download
            destination_path: Path where to save the file
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If receiving the file fails
        """
        logger.debug(f"Receiving file {file_id} to {destination_path}")
        # Ensure destination directory exists
        dest = Path(destination_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        resp = await self._client.send_command({
            "type": "receiveFile",
            "file_id": file_id,
            "file_path": str(dest.absolute())
        })
        
        await self._process_response(
            resp,
            "fileReceived",
            f"Failed to receive file {file_id}"
        )
        
        return self
    
    async def cancel(self, file_id: int) -> "FilesClient":
        """
        Cancel an ongoing file transfer.
        
        Args:
            file_id: ID of the file transfer to cancel
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If cancelling the file transfer fails
        """
        logger.debug(f"Cancelling file transfer {file_id}")
        resp = await self._client.send_command({
            "type": "cancelFile",
            "file_id": file_id
        })
        
        await self._process_response(
            resp,
            "fileCancelled",
            f"Failed to cancel file transfer {file_id}"
        )
        
        return self
    
    async def status(self, file_id: int) -> dict[str, Any]:
        """
        Get the status of a file transfer.
        
        Args:
            file_id: ID of the file transfer
            
        Returns:
            File transfer status information
            
        Raises:
            SimplexCommandError: If getting the status fails
        """
        logger.debug(f"Getting status for file transfer {file_id}")
        resp = await self._client.send_command({
            "type": "fileStatus",
            "file_id": file_id
        })
        
        resp = await self._process_response(
            resp,
            "fileStatusUpdated",
            f"Failed to get status for file {file_id}"
        )
        
        return getattr(resp, "fileTransfer", {})
    
    async def set_temp_folder(self, folder_path: str) -> "FilesClient":
        """
        Set the temporary folder for file downloads.
        
        Args:
            folder_path: Path to the temporary folder
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If setting the temp folder fails
            NotADirectoryError: If the specified path is not a directory
        """
        logger.debug(f"Setting temp folder to {folder_path}")
        # Verify directory exists or create it
        folder = Path(folder_path)
        if folder.exists() and not folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {folder_path}")
            
        folder.mkdir(parents=True, exist_ok=True)
        
        resp = await self._client.send_command({
            "type": "setTempFolder",
            "temp_folder_path": str(folder.absolute())
        })
        
        await self._process_response(
            resp,
            "tempFolderSet",
            f"Failed to set temp folder to {folder_path}"
        )
        
        return self
    
    async def set_files_folder(self, folder_path: str) -> "FilesClient":
        """
        Set the default folder for file downloads.
        
        Args:
            folder_path: Path to the files folder
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If setting the files folder fails
            NotADirectoryError: If the specified path is not a directory
        """
        logger.debug(f"Setting files folder to {folder_path}")
        # Verify directory exists or create it
        folder = Path(folder_path)
        if folder.exists() and not folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {folder_path}")
            
        folder.mkdir(parents=True, exist_ok=True)
        
        resp = await self._client.send_command({
            "type": "setFilesFolder",
            "files_folder_path": str(folder.absolute())
        })
        
        await self._process_response(
            resp,
            "filesFolderSet",
            f"Failed to set files folder to {folder_path}"
        )
        
        return self
