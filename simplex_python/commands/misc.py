"""
Miscellaneous commands for Simplex messaging system.

This module defines command classes for various operations:
- Setting incognito mode
- Managing addresses and connections
- Contact verification
- Server configuration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import BaseCommand, ServerProtocol
from ..models.archive import AutoAccept
from ..models.server import ServerCfg


@dataclass(kw_only=True)
class SetIncognito(BaseCommand):
    """Command to set incognito mode.

    Attributes:
        type: Command type identifier ("setIncognito").
        incognito: Whether to enable incognito mode.
    """

    type: str = "setIncognito"
    incognito: bool


@dataclass(kw_only=True)
class AddContact(BaseCommand):
    """Command to add a contact.

    Attributes:
        type: Command type identifier ("addContact").
    """

    type: str = "addContact"


@dataclass(kw_only=True)
class Connect(BaseCommand):
    """Command to connect using a connection request.

    Attributes:
        type: Command type identifier ("connect").
        conn_req: Connection request string.
    """

    type: str = "connect"
    conn_req: str


@dataclass(kw_only=True)
class ConnectSimplex(BaseCommand):
    """Command to connect to Simplex network.

    Attributes:
        type: Command type identifier ("connectSimplex").
    """

    type: str = "connectSimplex"


@dataclass(kw_only=True)
class APIContactInfo(BaseCommand):
    """Command to get contact information.

    Attributes:
        type: Command type identifier ("apiContactInfo").
        contact_id: Contact identifier.
    """

    type: str = "apiContactInfo"
    contact_id: int


@dataclass(kw_only=True)
class APIGetContactCode(BaseCommand):
    """Command to get a verification code for a contact.

    Attributes:
        type: Command type identifier ("apiGetContactCode").
        contact_id: Contact identifier.
    """

    type: str = "apiGetContactCode"
    contact_id: int


@dataclass(kw_only=True)
class APIVerifyContact(BaseCommand):
    """Command to verify a contact using a connection code.

    Attributes:
        type: Command type identifier ("apiVerifyContact").
        contact_id: Contact identifier.
        connection_code: Connection verification code.
    """

    type: str = "apiVerifyContact"
    contact_id: int
    connection_code: Optional[str] = None


@dataclass(kw_only=True)
class CreateMyAddress(BaseCommand):
    """Command to create a user address.

    Attributes:
        type: Command type identifier ("createMyAddress").
    """

    type: str = "createMyAddress"


@dataclass(kw_only=True)
class DeleteMyAddress(BaseCommand):
    """Command to delete a user address.

    Attributes:
        type: Command type identifier ("deleteMyAddress").
    """

    type: str = "deleteMyAddress"


@dataclass(kw_only=True)
class ShowMyAddress(BaseCommand):
    """Command to show a user address.

    Attributes:
        type: Command type identifier ("showMyAddress").
    """

    type: str = "showMyAddress"


@dataclass(kw_only=True)
class SetProfileAddress(BaseCommand):
    """Command to set a profile address.

    Attributes:
        type: Command type identifier ("setProfileAddress").
        include_in_profile: Whether to include address in profile.
    """

    type: str = "setProfileAddress"
    include_in_profile: bool


@dataclass(kw_only=True)
class AddressAutoAccept(BaseCommand):
    """Command to configure auto-accept for a user address.

    Attributes:
        type: Command type identifier ("addressAutoAccept").
        auto_accept: Optional auto-accept configuration.
    """

    type: str = "addressAutoAccept"
    auto_accept: Optional[AutoAccept] = None


@dataclass(kw_only=True)
class APICreateMyAddress(BaseCommand):
    """Command to create a user address via API.

    Attributes:
        type: Command type identifier ("apiCreateMyAddress").
        user_id: User identifier.
    """

    type: str = "apiCreateMyAddress"
    user_id: int


@dataclass(kw_only=True)
class APIDeleteMyAddress(BaseCommand):
    """Command to delete a user address via API.

    Attributes:
        type: Command type identifier ("apiDeleteMyAddress").
        user_id: User identifier.
    """

    type: str = "apiDeleteMyAddress"
    user_id: int


@dataclass(kw_only=True)
class APIShowMyAddress(BaseCommand):
    """Command to show a user address via API.

    Attributes:
        type: Command type identifier ("apiShowMyAddress").
        user_id: User identifier.
    """

    type: str = "apiShowMyAddress"
    user_id: int


@dataclass(kw_only=True)
class APISetProfileAddress(BaseCommand):
    """Command to set a profile address via API.

    Attributes:
        type: Command type identifier ("apiSetProfileAddress").
        user_id: User identifier.
        include_in_profile: Whether to include address in profile.
    """

    type: str = "apiSetProfileAddress"
    user_id: int
    include_in_profile: bool


@dataclass(kw_only=True)
class APIAddressAutoAccept(BaseCommand):
    """Command to configure auto-accept for a user address via API.

    Attributes:
        type: Command type identifier ("apiAddressAutoAccept").
        user_id: User identifier.
        auto_accept: Optional auto-accept configuration.
    """

    type: str = "apiAddressAutoAccept"
    user_id: int
    auto_accept: Optional[AutoAccept] = None


@dataclass(kw_only=True)
class APIGetUserProtoServers(BaseCommand):
    """Command to get a user's protocol servers.

    Attributes:
        type: Command type identifier ("apiGetUserProtoServers").
        user_id: User identifier.
        server_protocol: Protocol type.
    """

    type: str = "apiGetUserProtoServers"
    user_id: int
    server_protocol: ServerProtocol


@dataclass(kw_only=True)
class APISetUserProtoServers(BaseCommand):
    """Command to set a user's protocol servers.

    Attributes:
        type: Command type identifier ("apiSetUserProtoServers").
        user_id: User identifier.
        server_protocol: Protocol type.
        servers: List of server configurations.
    """

    type: str = "apiSetUserProtoServers"
    user_id: int
    server_protocol: ServerProtocol
    servers: List[ServerCfg]
