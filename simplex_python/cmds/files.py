"""
File management command classes for the Simplex messaging system.

This module defines the commands for managing files, including:
- Setting file and temporary folder locations
- Receiving and managing file transfers
- Checking file status

All commands inherit from BaseCommand and provide a consistent interface
for file-related operations in the Simplex system.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union
from .base import BaseCommand


@dataclass(kw_only=True)
class SetTempFolder(BaseCommand):
    """Command to set the temporary folder for file operations."""

    type: str = "setTempFolder"
    tempFolder: str


@dataclass(kw_only=True)
class SetFilesFolder(BaseCommand):
    """Command to set the files folder for file storage."""

    type: str = "setFilesFolder"
    filePath: str


@dataclass(kw_only=True)
class ReceiveFile(BaseCommand):
    """Command to receive a file."""

    type: str = "receiveFile"
    fileId: int
    filePath: Optional[str] = None


@dataclass(kw_only=True)
class CancelFile(BaseCommand):
    """Command to cancel a file transfer."""

    type: str = "cancelFile"
    fileId: int


@dataclass(kw_only=True)
class FileStatus(BaseCommand):
    """Command to check the status of a file transfer."""

    type: str = "fileStatus"
    fileId: int


# Type alias for FileCommand
FileCommand = Union[
    SetTempFolder,
    SetFilesFolder,
    ReceiveFile,
    CancelFile,
    FileStatus,
]
