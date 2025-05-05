"""
Database-related response types for the Simplex messaging system.

This module defines response types for database operations, including:
- Archive export and import confirmations
- Storage deletion confirmations
- Database operation errors

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .base import CommandResponse


@dataclass
class ExportArchiveProgressResponse(CommandResponse):
    """Response showing export archive operation progress."""

    progress: float = 0.0
    total: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExportArchiveProgressResponse":
        return cls(
            type="exportArchiveProgress",
            user=data.get("user"),
            progress=data.get("progress", 0.0),
            total=data.get("total"),
        )


@dataclass
class ExportArchiveCompletedResponse(CommandResponse):
    """Response when archive export is completed."""

    archivePath: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExportArchiveCompletedResponse":
        return cls(
            type="exportArchiveCompleted",
            user=data.get("user"),
            archivePath=data.get("archivePath", ""),
        )


@dataclass
class ExportArchiveErrorResponse(CommandResponse):
    """Response when there is an error with archive export."""

    errorMessage: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExportArchiveErrorResponse":
        return cls(
            type="exportArchiveError",
            user=data.get("user"),
            errorMessage=data.get("errorMessage", ""),
        )


@dataclass
class ImportArchiveProgressResponse(CommandResponse):
    """Response showing import archive operation progress."""

    progress: float = 0.0
    total: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImportArchiveProgressResponse":
        return cls(
            type="importArchiveProgress",
            user=data.get("user"),
            progress=data.get("progress", 0.0),
            total=data.get("total"),
        )


@dataclass
class ImportArchiveCompletedResponse(CommandResponse):
    """Response when archive import is completed."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImportArchiveCompletedResponse":
        return cls(type="importArchiveCompleted", user=data.get("user"))


@dataclass
class ImportArchiveErrorResponse(CommandResponse):
    """Response when there is an error with archive import."""

    errorMessage: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImportArchiveErrorResponse":
        return cls(
            type="importArchiveError",
            user=data.get("user"),
            errorMessage=data.get("errorMessage", ""),
        )


@dataclass
class DeleteStorageCompletedResponse(CommandResponse):
    """Response when storage deletion is completed."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeleteStorageCompletedResponse":
        return cls(type="deleteStorageCompleted", user=data.get("user"))


@dataclass
class DeleteStorageErrorResponse(CommandResponse):
    """Response when there is an error with storage deletion."""

    errorMessage: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeleteStorageErrorResponse":
        return cls(
            type="deleteStorageError",
            user=data.get("user"),
            errorMessage=data.get("errorMessage", ""),
        )


# Type alias for database-related responses
DatabaseResponse = (
    ExportArchiveProgressResponse
    | ExportArchiveCompletedResponse
    | ExportArchiveErrorResponse
    | ImportArchiveProgressResponse
    | ImportArchiveCompletedResponse
    | ImportArchiveErrorResponse
    | DeleteStorageCompletedResponse
    | DeleteStorageErrorResponse
)
