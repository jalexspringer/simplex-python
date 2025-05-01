"""
Server configuration models for Simplex network.

This module defines the structures for server configurations used in the Simplex system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from ..commands.base import ServerProtocol


@dataclass(kw_only=True)
class ServerCfg:
    """Server configuration.

    Attributes:
        server: Server address.
        preset: Whether this is a preset server.
        tested: Whether this server has been tested.
        enabled: Whether this server is enabled.
    """

    server: str
    preset: bool
    enabled: bool
    tested: Optional[bool] = None
