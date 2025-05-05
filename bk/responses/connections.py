"""
Connection-related response types for the Simplex messaging system.

This module defines response types for connection operations, including:
- Contact request responses (acceptance, rejection)
- Connection establishment notifications
- Contact information updates
- Server configuration responses

All responses follow a consistent pattern with the command classes they correspond to.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .base import CommandResponse


@dataclass
class ContactRequestRejectedResponse(CommandResponse):
    """Response when a contact request is rejected."""

    contactRequest: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactRequestRejectedResponse":
        return cls(
            type="contactRequestRejected",
            user=data.get("user"),
            contactRequest=data.get("contactRequest", {}),
        )


@dataclass
class ReceivedContactRequestResponse(CommandResponse):
    """Response when a new contact request is received."""

    contactRequest: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReceivedContactRequestResponse":
        return cls(
            type="receivedContactRequest",
            user=data.get("user"),
            contactRequest=data.get("contactRequest", {}),
        )


@dataclass
class AcceptingContactRequestResponse(CommandResponse):
    """Response when a contact request is being accepted."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AcceptingContactRequestResponse":
        return cls(
            type="acceptingContactRequest",
            user=data.get("user"),
            contact=data.get("contact", {}),
        )


@dataclass
class ContactAlreadyExistsResponse(CommandResponse):
    """Response when attempting to add a contact that already exists."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactAlreadyExistsResponse":
        return cls(
            type="contactAlreadyExists",
            user=data.get("user"),
            contact=data.get("contact", {}),
        )


@dataclass
class ContactRequestAlreadyAcceptedResponse(CommandResponse):
    """Response when a contact request has already been accepted."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactRequestAlreadyAcceptedResponse":
        return cls(
            type="contactRequestAlreadyAccepted",
            user=data.get("user"),
            contact=data.get("contact", {}),
        )


@dataclass
class ContactInfoResponse(CommandResponse):
    """Response containing contact information."""

    contact: Dict[str, Any] = field(default_factory=dict)
    connectionStats: Dict[str, Any] = field(default_factory=dict)
    customUserProfile: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactInfoResponse":
        return cls(
            type="contactInfo",
            user=data.get("user"),
            contact=data.get("contact", {}),
            connectionStats=data.get("connectionStats", {}),
            customUserProfile=data.get("customUserProfile"),
        )


@dataclass
class ContactAliasUpdatedResponse(CommandResponse):
    """Response when a contact's alias is updated."""

    toContact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactAliasUpdatedResponse":
        return cls(
            type="contactAliasUpdated",
            user=data.get("user"),
            toContact=data.get("toContact", {}),
        )


@dataclass
class ContactConnectingResponse(CommandResponse):
    """Response when a connection to a contact is being established."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactConnectingResponse":
        return cls(
            type="contactConnecting",
            user=data.get("user"),
            contact=data.get("contact", {}),
        )


@dataclass
class ContactConnectedResponse(CommandResponse):
    """Response when a connection to a contact is established."""

    contact: Dict[str, Any] = field(default_factory=dict)
    userCustomProfile: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactConnectedResponse":
        return cls(
            type="contactConnected",
            user=data.get("user"),
            contact=data.get("contact", {}),
            userCustomProfile=data.get("userCustomProfile"),
        )


@dataclass
class ContactUpdatedResponse(CommandResponse):
    """Response when a contact is updated."""

    fromContact: Dict[str, Any] = field(default_factory=dict)
    toContact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactUpdatedResponse":
        return cls(
            type="contactUpdated",
            user=data.get("user"),
            fromContact=data.get("fromContact", {}),
            toContact=data.get("toContact", {}),
        )


@dataclass
class ContactsMergedResponse(CommandResponse):
    """Response when contacts are merged."""

    intoContact: Dict[str, Any] = field(default_factory=dict)
    mergedContact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactsMergedResponse":
        return cls(
            type="contactsMerged",
            user=data.get("user"),
            intoContact=data.get("intoContact", {}),
            mergedContact=data.get("mergedContact", {}),
        )


@dataclass
class ContactDeletedResponse(CommandResponse):
    """Response when a contact is deleted."""

    contact: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactDeletedResponse":
        return cls(
            type="contactDeleted",
            user=data.get("user"),
            contact=data.get("contact", {}),
        )


@dataclass
class ContactSubErrorResponse(CommandResponse):
    """Response when there is an error with a contact subscription."""

    contact: Dict[str, Any] = field(default_factory=dict)
    chatError: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactSubErrorResponse":
        return cls(
            type="contactSubError",
            user=data.get("user"),
            contact=data.get("contact", {}),
            chatError=data.get("chatError", {}),
        )


@dataclass
class ContactSubSummaryResponse(CommandResponse):
    """Response containing a summary of contact subscriptions."""

    contactSubscriptions: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactSubSummaryResponse":
        return cls(
            type="contactSubSummary",
            user=data.get("user"),
            contactSubscriptions=data.get("contactSubscriptions", []),
        )


@dataclass
class ContactsDisconnectedResponse(CommandResponse):
    """Response when contacts are disconnected."""

    server: str = ""
    contactRefs: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactsDisconnectedResponse":
        return cls(
            type="contactsDisconnected",
            user=data.get("user"),
            server=data.get("server", ""),
            contactRefs=data.get("contactRefs", []),
        )


@dataclass
class ContactsSubscribedResponse(CommandResponse):
    """Response when contacts are subscribed."""

    server: str = ""
    contactRefs: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactsSubscribedResponse":
        return cls(
            type="contactsSubscribed",
            user=data.get("user"),
            server=data.get("server", ""),
            contactRefs=data.get("contactRefs", []),
        )


@dataclass
class HostConnectedResponse(CommandResponse):
    """Response when a host connection is established."""

    protocol: str = ""
    transportHost: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HostConnectedResponse":
        return cls(
            type="hostConnected",
            protocol=data.get("protocol", ""),
            transportHost=data.get("transportHost", ""),
        )


@dataclass
class HostDisconnectedResponse(CommandResponse):
    """Response when a host connection is disconnected."""

    protocol: str = ""
    transportHost: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HostDisconnectedResponse":
        return cls(
            type="hostDisconnected",
            protocol=data.get("protocol", ""),
            transportHost=data.get("transportHost", ""),
        )


@dataclass
class UserProtoServersResponse(CommandResponse):
    """Response containing user protocol server information."""

    servers: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProtoServersResponse":
        return cls(
            type="userProtoServers",
            user=data.get("user"),
            servers=data.get("servers", {}),
        )


@dataclass
class InvitationResponse(CommandResponse):
    """Response containing a connection invitation."""

    connReqInvitation: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvitationResponse":
        return cls(
            type="invitation",
            user=data.get("user"),
            connReqInvitation=data.get("connReqInvitation", ""),
        )


@dataclass
class SentConfirmationResponse(CommandResponse):
    """Response when a confirmation is sent."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SentConfirmationResponse":
        return cls(type="sentConfirmation", user=data.get("user"))


@dataclass
class SentInvitationResponse(CommandResponse):
    """Response when an invitation is sent."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SentInvitationResponse":
        return cls(type="sentInvitation", user=data.get("user"))


@dataclass
class ContactConnectionDeletedResponse(CommandResponse):
    """Response when a contact connection is deleted."""

    connection: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactConnectionDeletedResponse":
        return cls(
            type="contactConnectionDeleted",
            user=data.get("user"),
            connection=data.get("connection", {}),
        )


# Supporting data classes
@dataclass
class ContactRef:
    """Reference to a contact."""

    contactId: int
    localDisplayName: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactRef":
        return cls(
            contactId=data.get("contactId", 0),
            localDisplayName=data.get("localDisplayName", ""),
        )


@dataclass
class ConnectionStats:
    """Statistics for a connection."""

    rcvServers: Optional[List[str]] = None
    sndServers: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectionStats":
        return cls(rcvServers=data.get("rcvServers"), sndServers=data.get("sndServers"))


# Type alias for connection-related responses
ConnectionResponse = (
    ContactRequestRejectedResponse
    | ReceivedContactRequestResponse
    | AcceptingContactRequestResponse
    | ContactAlreadyExistsResponse
    | ContactRequestAlreadyAcceptedResponse
    | ContactInfoResponse
    | ContactAliasUpdatedResponse
    | ContactConnectingResponse
    | ContactConnectedResponse
    | ContactUpdatedResponse
    | ContactsMergedResponse
    | ContactDeletedResponse
    | ContactSubErrorResponse
    | ContactSubSummaryResponse
    | ContactsDisconnectedResponse
    | ContactsSubscribedResponse
    | HostConnectedResponse
    | HostDisconnectedResponse
    | UserProtoServersResponse
    | InvitationResponse
    | SentConfirmationResponse
    | SentInvitationResponse
    | ContactConnectionDeletedResponse
)
