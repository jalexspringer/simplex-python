"""
Pagination models for Simplex chat queries.

This module defines the structures for pagination used in chat and item operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class ChatPagination:
    """Pagination parameters for chat queries.

    Attributes:
        count: Number of items to retrieve.
        after: Optional ID to start after.
        before: Optional ID to end before.
    """

    count: int
    after: Optional[int] = None
    before: Optional[int] = None


@dataclass(kw_only=True)
class ItemRange:
    """Range of chat items.

    Attributes:
        from_item: Starting item ID.
        to_item: Ending item ID.
    """

    from_item: int
    to_item: int
