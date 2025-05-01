"""
File-related responses for Simplex messaging system.

This module defines response classes for file transfer operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .base import BaseResponse, ChatResponseType
from ..models.chat import (
    User,
    AChatItem,
    RcvFileTransfer,
    SndFileTransfer,
    FileTransferMeta,
    ChatError,
)


@dataclass(kw_only=True)
class CRRcvFileAccepted(BaseResponse):
    """Response for received file accepted.

    Attributes:
        type: Response type identifier ("rcvFileAccepted").
        user: User information.
        chat_item: Chat item information.
    """

    type: str = ChatResponseType.RCV_FILE_ACCEPTED.value
    user: User
    chat_item: AChatItem


@dataclass(kw_only=True)
class CRRcvFileAcceptedSndCancelled(BaseResponse):
    """Response for received file accepted but sender cancelled.

    Attributes:
        type: Response type identifier ("rcvFileAcceptedSndCancelled").
        user: User information.
        rcv_file_transfer: Received file transfer information.
    """

    type: str = ChatResponseType.RCV_FILE_ACCEPTED_SND_CANCELLED.value
    user: User
    rcv_file_transfer: RcvFileTransfer


@dataclass(kw_only=True)
class CRRcvFileStart(BaseResponse):
    """Response for received file transfer started.

    Attributes:
        type: Response type identifier ("rcvFileStart").
        user: User information.
        chat_item: Chat item information.
    """

    type: str = ChatResponseType.RCV_FILE_START.value
    user: User
    chat_item: AChatItem


@dataclass(kw_only=True)
class CRRcvFileComplete(BaseResponse):
    """Response for received file transfer completed.

    Attributes:
        type: Response type identifier ("rcvFileComplete").
        user: User information.
        chat_item: Chat item information.
    """

    type: str = ChatResponseType.RCV_FILE_COMPLETE.value
    user: User
    chat_item: AChatItem


@dataclass(kw_only=True)
class CRRcvFileCancelled(BaseResponse):
    """Response for received file transfer cancelled.

    Attributes:
        type: Response type identifier ("rcvFileCancelled").
        user: User information.
        rcv_file_transfer: Received file transfer information.
    """

    type: str = ChatResponseType.RCV_FILE_CANCELLED.value
    user: User
    rcv_file_transfer: RcvFileTransfer


@dataclass(kw_only=True)
class CRRcvFileSndCancelled(BaseResponse):
    """Response for received file transfer cancelled by sender.

    Attributes:
        type: Response type identifier ("rcvFileSndCancelled").
        user: User information.
        rcv_file_transfer: Received file transfer information.
    """

    type: str = ChatResponseType.RCV_FILE_SND_CANCELLED.value
    user: User
    rcv_file_transfer: RcvFileTransfer


@dataclass(kw_only=True)
class CRSndFileStart(BaseResponse):
    """Response for sent file transfer started.

    Attributes:
        type: Response type identifier ("sndFileStart").
        user: User information.
        chat_item: Chat item information.
        snd_file_transfer: Sent file transfer information.
    """

    type: str = ChatResponseType.SND_FILE_START.value
    user: User
    chat_item: AChatItem
    snd_file_transfer: SndFileTransfer


@dataclass(kw_only=True)
class CRSndFileComplete(BaseResponse):
    """Response for sent file transfer completed.

    Attributes:
        type: Response type identifier ("sndFileComplete").
        user: User information.
        chat_item: Chat item information.
        snd_file_transfer: Sent file transfer information.
    """

    type: str = ChatResponseType.SND_FILE_COMPLETE.value
    user: User
    chat_item: AChatItem
    snd_file_transfer: SndFileTransfer


@dataclass(kw_only=True)
class CRSndFileCancelled(BaseResponse):
    """Response for sent file transfer cancelled.

    Attributes:
        type: Response type identifier ("sndFileCancelled").
        user: User information.
        chat_item: Chat item information.
        snd_file_transfer: Sent file transfer information.
    """

    type: str = ChatResponseType.SND_FILE_CANCELLED.value
    user: User
    chat_item: AChatItem
    snd_file_transfer: SndFileTransfer


@dataclass(kw_only=True)
class CRSndFileRcvCancelled(BaseResponse):
    """Response for sent file transfer cancelled by receiver.

    Attributes:
        type: Response type identifier ("sndFileRcvCancelled").
        user: User information.
        chat_item: Chat item information.
        snd_file_transfer: Sent file transfer information.
    """

    type: str = ChatResponseType.SND_FILE_RCV_CANCELLED.value
    user: User
    chat_item: AChatItem
    snd_file_transfer: SndFileTransfer


@dataclass(kw_only=True)
class CRSndGroupFileCancelled(BaseResponse):
    """Response for sent group file transfer cancelled.

    Attributes:
        type: Response type identifier ("sndGroupFileCancelled").
        user: User information.
        chat_item: Chat item information.
        file_transfer_meta: File transfer metadata.
        snd_file_transfers: List of sent file transfer information.
    """

    type: str = ChatResponseType.SND_GROUP_FILE_CANCELLED.value
    user: User
    chat_item: AChatItem
    file_transfer_meta: FileTransferMeta
    snd_file_transfers: List[SndFileTransfer]


@dataclass(kw_only=True)
class CRSndFileSubError(BaseResponse):
    """Response for sent file subscription error.

    Attributes:
        type: Response type identifier ("sndFileSubError").
        user: User information.
        snd_file_transfer: Sent file transfer information.
        chat_error: Chat error information.
    """

    type: str = ChatResponseType.SND_FILE_SUB_ERROR.value
    user: User
    snd_file_transfer: SndFileTransfer
    chat_error: ChatError


@dataclass(kw_only=True)
class CRRcvFileSubError(BaseResponse):
    """Response for received file subscription error.

    Attributes:
        type: Response type identifier ("rcvFileSubError").
        user: User information.
        rcv_file_transfer: Received file transfer information.
        chat_error: Chat error information.
    """

    type: str = ChatResponseType.RCV_FILE_SUB_ERROR.value
    user: User
    rcv_file_transfer: RcvFileTransfer
    chat_error: ChatError
