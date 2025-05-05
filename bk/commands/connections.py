"""
Connection management command classes for the Simplex messaging system.

This module defines the commands for managing connections, including:
- Accepting and rejecting contact requests
- Managing contact information and aliases
- Establishing connections
- Configuring server protocols

All commands inherit from BaseCommand and provide a consistent interface
for connection-related operations in the Simplex system.
"""

from dataclasses import dataclass
from typing import List, Union
from .base import BaseCommand, ServerProtocol, ServerCfg


@dataclass(kw_only=True)
class APIAcceptContact(BaseCommand):
    """Command to accept a contact request via API."""

    type: str = "apiAcceptContact"
    contactReqId: int


@dataclass(kw_only=True)
class APIRejectContact(BaseCommand):
    """Command to reject a contact request via API."""

    type: str = "apiRejectContact"
    contactReqId: int


@dataclass(kw_only=True)
class APISetContactAlias(BaseCommand):
    """Command to set a contact's alias via API."""

    type: str = "apiSetContactAlias"
    contactId: int
    localAlias: str


@dataclass(kw_only=True)
class APIContactInfo(BaseCommand):
    """Command to get contact information via API."""

    type: str = "apiContactInfo"
    contactId: int


@dataclass(kw_only=True)
class APIGetContactCode(BaseCommand):
    """Command to get a contact verification code via API."""

    type: str = "apiGetContactCode"
    contactId: int


@dataclass(kw_only=True)
class APIVerifyContact(BaseCommand):
    """Command to verify a contact via API."""

    type: str = "apiVerifyContact"
    contactId: int
    connectionCode: str


@dataclass(kw_only=True)
class AddContact(BaseCommand):
    """Command to add a contact."""

    type: str = "addContact"


@dataclass(kw_only=True)
class Connect(BaseCommand):
    """Command to connect with a connection request."""

    type: str = "connect"
    connReq: str


@dataclass(kw_only=True)
class ConnectSimplex(BaseCommand):
    """Command to connect with Simplex."""

    type: str = "connectSimplex"


@dataclass(kw_only=True)
class APIGetUserProtoServers(BaseCommand):
    """Command to get user protocol servers via API."""

    type: str = "apiGetUserProtoServers"
    userId: int
    serverProtocol: ServerProtocol


@dataclass(kw_only=True)
class APISetUserProtoServers(BaseCommand):
    """Command to set user protocol servers via API."""

    type: str = "apiSetUserProtoServers"
    userId: int
    serverProtocol: ServerProtocol
    servers: List[ServerCfg]


# Type alias for ConnectionCommand
ConnectionCommand = Union[
    APIAcceptContact,
    APIRejectContact,
    APISetContactAlias,
    APIContactInfo,
    APIGetContactCode,
    APIVerifyContact,
    AddContact,
    Connect,
    ConnectSimplex,
    APIGetUserProtoServers,
    APISetUserProtoServers,
]
