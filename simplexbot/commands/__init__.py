"""Aggregate exports for *simplexbot.commands* package.

This allows callers to do:

    from simplexbot.commands import StartChat, ShowActiveUser, ...

without needing to know the exact sub-module where a command is defined.
"""

from importlib import import_module as _imp
from types import ModuleType as _ModuleType
from typing import TYPE_CHECKING as _T

# Sub-modules we always expose
_submods: dict[str, str] = {
    # always keep base first so enums are available to others
    "base": "simplexbot.commands.base",
    "user": "simplexbot.commands.user",
    "chat": "simplexbot.commands.chat",
}

for _alias, _path in _submods.items():
    globals()[_alias] = _imp(_path)  # type: ignore[str-bytes-safe]

# Re-export everything marked in sub-module __all__
__all__: list[str] = []
for _m in globals().values():
    if isinstance(_m, _ModuleType) and hasattr(_m, "__all__"):
        __all__.extend(_m.__all__)  # type: ignore[arg-type]

# Keep mypy happy on direct import usage
if _T:
    from .base import *  # noqa: F401,F403
    from .user import *  # noqa: F401,F403
    from .chat import *  # noqa: F401,F403
