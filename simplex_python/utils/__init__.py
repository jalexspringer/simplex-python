"""
Utility modules for the Simplex Python client.

This package contains various utility functions used by the Simplex client.
"""

from .command_formatting import (
    cmd_string,
    on_off,
    maybe,
    maybe_json,
    pagination_str,
    auto_accept_str,
)

__all__ = [
    "cmd_string",
    "on_off",
    "maybe",
    "maybe_json",
    "pagination_str",
    "auto_accept_str",
]
