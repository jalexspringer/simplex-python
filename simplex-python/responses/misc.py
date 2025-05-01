"""
Miscellaneous responses for Simplex messaging system.

This module defines response classes for various operations not fitting other categories.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .base import BaseResponse, ChatResponseType
from ..models.chat import User, PendingSubStatus


@dataclass(kw_only=True)
class CRPendingSubSummary(BaseResponse):
    """Response for pending subscription summary.

    Attributes:
        type: Response type identifier ("pendingSubSummary").
        user: User information.
        pending_sub_status: List of pending subscription status.
    """

    type: str = ChatResponseType.PENDING_SUB_SUMMARY.value
    user: User
    pending_sub_status: List[PendingSubStatus]
