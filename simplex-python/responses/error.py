"""
Error responses for Simplex messaging system.

This module defines response classes for errors and failures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import BaseResponse, ChatResponseType
from ..models.chat import User, ChatError


@dataclass(kw_only=True)
class CRMessageError(BaseResponse):
    """Response for message error.

    Attributes:
        type: Response type identifier ("messageError").
        user: User information.
        severity: Error severity.
        error_message: Error message.
    """

    type: str = ChatResponseType.MESSAGE_ERROR.value
    user: User
    severity: str
    error_message: str


@dataclass(kw_only=True)
class CRChatCmdError(BaseResponse):
    """Response for chat command error.

    Attributes:
        type: Response type identifier ("chatCmdError").
        chat_error: Chat error information.
        user_: Optional user information.
    """

    type: str = ChatResponseType.CHAT_CMD_ERROR.value
    chat_error: ChatError
    user_: Optional[User] = None


@dataclass(kw_only=True)
class CRChatError(BaseResponse):
    """Response for chat error.

    Attributes:
        type: Response type identifier ("chatError").
        chat_error: Chat error information.
        user_: Optional user information.
    """

    type: str = ChatResponseType.CHAT_ERROR.value
    chat_error: ChatError
    user_: Optional[User] = None
