"""
File transfer commands for Simplex messaging system.

This module defines command classes for file transfer operations:
- Receiving and downloading files
- Canceling file transfers
- Checking file transfer status
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseCommand


@dataclass(kw_only=True)
class ReceiveFile(BaseCommand):
    """Command to receive a file.

    Attributes:
        type: Command type identifier ("receiveFile").
        file_id: File identifier to receive.
        file_path: Optional destination path for the file.
    """

    type: str = "receiveFile"
    file_id: int
    file_path: Optional[str] = None


@dataclass(kw_only=True)
class CancelFile(BaseCommand):
    """Command to cancel a file transfer.

    Attributes:
        type: Command type identifier ("cancelFile").
        file_id: File identifier to cancel.
    """

    type: str = "cancelFile"
    file_id: int


@dataclass(kw_only=True)
class FileStatus(BaseCommand):
    """Command to check file transfer status.

    Attributes:
        type: Command type identifier ("fileStatus").
        file_id: File identifier to check.
    """

    type: str = "fileStatus"
    file_id: int
