"""
File-related response types for the Simplex messaging system.

This module defines response types for file-related operations, including:
- File transfer status updates (started, completed, cancelled)
- File transfer error responses
- File reception confirmations

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .base import CommandResponse


@dataclass
class RcvFileAcceptedResponse(CommandResponse):
    """Response when a file receive request is accepted."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileAcceptedResponse":
        return cls(
            type="rcvFileAccepted",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
        )


@dataclass
class RcvFileStartResponse(CommandResponse):
    """Response when a file receive operation starts."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileStartResponse":
        return cls(
            type="rcvFileStart",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
        )


@dataclass
class RcvFileCompleteResponse(CommandResponse):
    """Response when a file receive operation completes."""

    chatItem: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileCompleteResponse":
        return cls(
            type="rcvFileComplete",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
        )


@dataclass
class RcvFileCancelledResponse(CommandResponse):
    """Response when a file receive operation is cancelled by the receiver."""

    rcvFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileCancelledResponse":
        return cls(
            type="rcvFileCancelled",
            user=data.get("user"),
            rcvFileTransfer=data.get("rcvFileTransfer", {}),
        )


@dataclass
class RcvFileSndCancelledResponse(CommandResponse):
    """Response when a file receive operation is cancelled by the sender."""

    rcvFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileSndCancelledResponse":
        return cls(
            type="rcvFileSndCancelled",
            user=data.get("user"),
            rcvFileTransfer=data.get("rcvFileTransfer", {}),
        )


@dataclass
class RcvFileAcceptedSndCancelledResponse(CommandResponse):
    """Response when a file is accepted by receiver but cancelled by sender."""

    rcvFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileAcceptedSndCancelledResponse":
        return cls(
            type="rcvFileAcceptedSndCancelled",
            user=data.get("user"),
            rcvFileTransfer=data.get("rcvFileTransfer", {}),
        )


@dataclass
class RcvFileSubErrorResponse(CommandResponse):
    """Response when there is an error with a file receive subscription."""

    rcvFileTransfer: Dict[str, Any] = field(default_factory=dict)
    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileSubErrorResponse":
        return cls(
            type="rcvFileSubError",
            user=data.get("user"),
            rcvFileTransfer=data.get("rcvFileTransfer", {}),
            chatError=data.get("chatError", {}),
        )


@dataclass
class SndFileStartResponse(CommandResponse):
    """Response when a file send operation starts."""

    chatItem: Dict[str, Any] = field(default_factory=dict)
    sndFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileStartResponse":
        return cls(
            type="sndFileStart",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
            sndFileTransfer=data.get("sndFileTransfer", {}),
        )


@dataclass
class SndFileCompleteResponse(CommandResponse):
    """Response when a file send operation completes."""

    chatItem: Dict[str, Any] = field(default_factory=dict)
    sndFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileCompleteResponse":
        return cls(
            type="sndFileComplete",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
            sndFileTransfer=data.get("sndFileTransfer", {}),
        )


@dataclass
class SndFileCancelledResponse(CommandResponse):
    """Response when a file send operation is cancelled by the sender."""

    chatItem: Dict[str, Any] = field(default_factory=dict)
    sndFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileCancelledResponse":
        return cls(
            type="sndFileCancelled",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
            sndFileTransfer=data.get("sndFileTransfer", {}),
        )


@dataclass
class SndFileRcvCancelledResponse(CommandResponse):
    """Response when a file send operation is cancelled by the receiver."""

    chatItem: Dict[str, Any] = field(default_factory=dict)
    sndFileTransfer: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileRcvCancelledResponse":
        return cls(
            type="sndFileRcvCancelled",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
            sndFileTransfer=data.get("sndFileTransfer", {}),
        )


@dataclass
class SndGroupFileCancelledResponse(CommandResponse):
    """Response when a group file send operation is cancelled."""

    chatItem: Dict[str, Any] = field(default_factory=dict)
    fileTransferMeta: Dict[str, Any] = field(default_factory=dict)
    sndFileTransfers: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndGroupFileCancelledResponse":
        return cls(
            type="sndGroupFileCancelled",
            user=data.get("user"),
            chatItem=data.get("chatItem", {}),
            fileTransferMeta=data.get("fileTransferMeta", {}),
            sndFileTransfers=data.get("sndFileTransfers", []),
        )


@dataclass
class SndFileSubErrorResponse(CommandResponse):
    """Response when there is an error with a file send subscription."""

    sndFileTransfer: Dict[str, Any] = field(default_factory=dict)
    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileSubErrorResponse":
        return cls(
            type="sndFileSubError",
            user=data.get("user"),
            sndFileTransfer=data.get("sndFileTransfer", {}),
            chatError=data.get("chatError", {}),
        )


# Supporting data classes
@dataclass
class RcvFileTransfer:
    """Information about a file being received."""

    fileId: int
    senderDisplayName: str
    chunkSize: int
    cancelled: bool = False
    grpMemberId: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RcvFileTransfer":
        return cls(
            fileId=data.get("fileId", 0),
            senderDisplayName=data.get("senderDisplayName", ""),
            chunkSize=data.get("chunkSize", 0),
            cancelled=data.get("cancelled", False),
            grpMemberId=data.get("grpMemberId"),
        )


@dataclass
class SndFileTransfer:
    """Information about a file being sent."""

    fileId: int
    fileName: str
    filePath: str
    fileSize: int
    chunkSize: int
    recipientDisplayName: str
    connId: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SndFileTransfer":
        return cls(
            fileId=data.get("fileId", 0),
            fileName=data.get("fileName", ""),
            filePath=data.get("filePath", ""),
            fileSize=data.get("fileSize", 0),
            chunkSize=data.get("chunkSize", 0),
            recipientDisplayName=data.get("recipientDisplayName", ""),
            connId=data.get("connId", 0),
        )


@dataclass
class FileTransferMeta:
    """Metadata about a file transfer."""

    fileId: int
    fileName: str
    filePath: str
    fileSize: int
    chunkSize: int
    cancelled: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileTransferMeta":
        return cls(
            fileId=data.get("fileId", 0),
            fileName=data.get("fileName", ""),
            filePath=data.get("filePath", ""),
            fileSize=data.get("fileSize", 0),
            chunkSize=data.get("chunkSize", 0),
            cancelled=data.get("cancelled", False),
        )


# Type alias for file-related responses
FileResponse = (
    RcvFileAcceptedResponse
    | RcvFileStartResponse
    | RcvFileCompleteResponse
    | RcvFileCancelledResponse
    | RcvFileSndCancelledResponse
    | RcvFileAcceptedSndCancelledResponse
    | RcvFileSubErrorResponse
    | SndFileStartResponse
    | SndFileCompleteResponse
    | SndFileCancelledResponse
    | SndFileRcvCancelledResponse
    | SndGroupFileCancelledResponse
    | SndFileSubErrorResponse
)
