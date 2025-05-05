"""
Database and storage command classes for the Simplex messaging system.

This module defines the commands for managing database operations, including:
- Exporting and importing archives
- Deleting storage data
- Managing archive configurations

All commands inherit from BaseCommand and provide a consistent interface
for database-related operations in the Simplex system.
"""

from dataclasses import dataclass
from typing import Optional, Union
from .base import BaseCommand


@dataclass
class ArchiveConfig:
    """Configuration for archive operations."""

    archivePath: str
    disableCompression: bool = False
    parentTempDirectory: Optional[str] = None


@dataclass(kw_only=True)
class APIExportArchive(BaseCommand):
    """Command to export an archive via API."""

    type: str = "apiExportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIImportArchive(BaseCommand):
    """Command to import an archive via API."""

    type: str = "apiImportArchive"
    config: ArchiveConfig


@dataclass(kw_only=True)
class APIDeleteStorage(BaseCommand):
    """Command to delete storage data via API."""

    type: str = "apiDeleteStorage"


# Type alias for DatabaseCommand
DatabaseCommand = Union[
    APIExportArchive,
    APIImportArchive,
    APIDeleteStorage,
]
