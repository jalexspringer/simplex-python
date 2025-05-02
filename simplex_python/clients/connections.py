"""
Connections domain client for SimplexClient.

Provides a fluent API for connection-related operations.
"""

import logging
from typing import List, TYPE_CHECKING
from ..commands import (
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
    ServerProtocol,
    ServerCfg,
)
from ..response import ChatResponse
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class ConnectionsClient:
    """
    Client for connection-related operations in SimplexClient.

    This client is accessed via the `connections` property of SimplexClient
    and provides methods for managing contacts, connection requests, and
    server configurations.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def accept_contact(self, contact_req_id: int) -> ChatResponse:
        """
        Accept a contact request.

        Args:
            contact_req_id: ID of the contact request to accept.

        Returns:
            ChatResponse containing the result of the accept operation.
        """
        cmd = APIAcceptContact(
            type="apiAcceptContact",
            contactReqId=contact_req_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to accept contact: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "contactAccepted" or similar
        expected_types = ["contactAccepted", "contactConnected"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to accept contact: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def reject_contact(self, contact_req_id: int) -> ChatResponse:
        """
        Reject a contact request.

        Args:
            contact_req_id: ID of the contact request to reject.

        Returns:
            ChatResponse containing the result of the reject operation.
        """
        cmd = APIRejectContact(
            type="apiRejectContact",
            contactReqId=contact_req_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to reject contact: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "contactRejected" or similar
        expected_types = ["contactRejected"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to reject contact: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def set_contact_alias(self, contact_id: int, alias: str) -> ChatResponse:
        """
        Set an alias for a contact.

        Args:
            contact_id: ID of the contact.
            alias: Alias to set for the contact.

        Returns:
            ChatResponse containing the result of the alias update.
        """
        cmd = APISetContactAlias(
            type="apiSetContactAlias",
            contactId=contact_id,
            localAlias=alias,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to set contact alias: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "contactAliasSet" or similar
        expected_types = ["contactAliasSet"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to set contact alias: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_contact_info(self, contact_id: int) -> ChatResponse:
        """
        Get information about a contact.

        Args:
            contact_id: ID of the contact.

        Returns:
            ChatResponse containing the contact information.
        """
        cmd = APIContactInfo(
            type="apiContactInfo",
            contactId=contact_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get contact info: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "contactInfo" or similar
        expected_types = ["contactInfo"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to get contact info: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_verification_code(self, contact_id: int) -> ChatResponse:
        """
        Get a verification code for a contact.

        Args:
            contact_id: ID of the contact.

        Returns:
            ChatResponse containing the verification code.
        """
        cmd = APIGetContactCode(
            type="apiGetContactCode",
            contactId=contact_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get verification code: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "connectionCode" or similar
        expected_types = ["connectionCode", "contactCode"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to get verification code: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def verify_contact(
        self, contact_id: int, connection_code: str
    ) -> ChatResponse:
        """
        Verify a contact using a connection code.

        Args:
            contact_id: ID of the contact to verify.
            connection_code: Verification code to use.

        Returns:
            ChatResponse containing the verification result.
        """
        cmd = APIVerifyContact(
            type="apiVerifyContact",
            contactId=contact_id,
            connectionCode=connection_code,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to verify contact: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "contactVerified" or similar
        expected_types = ["contactVerified", "verificationResult"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to verify contact: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def add_contact(self) -> ChatResponse:
        """
        Add a new contact.

        Returns:
            ChatResponse containing the result of the add operation.
        """
        cmd = AddContact(type="addContact")

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to add contact: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def connect(self, connection_request: str) -> ChatResponse:
        """
        Connect using a connection request string.

        Args:
            connection_request: The connection request string.

        Returns:
            ChatResponse containing the result of the connect operation.
        """
        cmd = Connect(
            type="connect",
            connReq=connection_request,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to connect: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response varies depending on the type of connection
        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def connect_simplex(self) -> ChatResponse:
        """
        Connect to the Simplex network.

        Returns:
            ChatResponse containing the result of the connect operation.
        """
        cmd = ConnectSimplex(type="connectSimplex")

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to connect to Simplex: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_protocol_servers(self, user_id: int, protocol: str) -> ChatResponse:
        """
        Get protocol servers for a user.

        Args:
            user_id: ID of the user.
            protocol: Protocol type (e.g., 'smp', 'xftp').

        Returns:
            ChatResponse containing the user's protocol servers.
        """
        # Convert string protocol to ServerProtocol enum if needed
        protocol_enum = protocol
        if isinstance(protocol, str):
            protocol_enum = ServerProtocol(protocol.lower())

        cmd = APIGetUserProtoServers(
            type="apiGetUserProtoServers",
            userId=user_id,
            serverProtocol=protocol_enum,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get protocol servers: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "userServers" or similar
        expected_types = ["userServers"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to get protocol servers: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def set_protocol_servers(
        self, user_id: int, protocol: str, servers: List[ServerCfg]
    ) -> ChatResponse:
        """
        Set protocol servers for a user.

        Args:
            user_id: ID of the user.
            protocol: Protocol type (e.g., 'smp', 'xftp').
            servers: List of server configurations to set.

        Returns:
            ChatResponse containing the result of the set operation.
        """
        # Convert string protocol to ServerProtocol enum if needed
        protocol_enum = protocol
        if isinstance(protocol, str):
            protocol_enum = ServerProtocol(protocol.lower())

        cmd = APISetUserProtoServers(
            type="apiSetUserProtoServers",
            userId=user_id,
            serverProtocol=protocol_enum,
            servers=servers,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to set protocol servers: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "userServersSet" or similar
        expected_types = ["userServersSet"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to set protocol servers: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp
