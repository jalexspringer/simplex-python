"""
Archive models for Simplex data import/export.

This module defines the structures for archive configuration used in the Simplex system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(kw_only=True)
class ArchiveConfig:
    """Configuration for chat archive import/export.

    Attributes:
        archive_path: Path to the archive file.
        disable_compression: Whether to disable compression.
        parent_temp_directory: Parent directory for temporary files.
    """

    archive_path: str
    disable_compression: Optional[bool] = None
    parent_temp_directory: Optional[str] = None


@dataclass(kw_only=True)
class AutoAccept:
    """Auto-accept configuration for incoming connections.

    Attributes:
        accept_incognito: Whether to accept incognito connections.
        auto_reply: Optional automatic reply message content.
    """

    accept_incognito: bool
    auto_reply: Optional[Dict[str, Any]] = None
