"""
Users domain client for SimplexClient.

Provides a fluent API for user-related operations.
"""

import logging
from typing import Optional, TYPE_CHECKING, Dict

from simplex_python.responses import (
    ActiveUserResponse,
    UserContactLinkResponse,
    CommandResponse,
)
from ..commands import (
    ShowActiveUser,
    CreateActiveUser,
    Profile,
    CreateMyAddress,
    DeleteMyAddress,
    ShowMyAddress,
    AddressAutoAccept,
    APISetActiveUser,
    MCText,
)
from ..client_errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class UsersClient:
    """
    Client for user-related operations in SimplexClient.

    This client is accessed via the `users` property of SimplexClient
    and provides methods for managing user profiles and contact addresses.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def get_active(self) -> Optional[ActiveUserResponse]:
        """
        Get the currently active user profile.

        Returns:
            ActiveUserResponse containing the user profile object, or None if no active user exists.

        Raises:
            SimplexCommandError: If there was an error executing the command.
        """
        cmd = ShowActiveUser(type="showActiveUser")
        resp = await self._client.send_command(cmd)
        
        # If we got None back, it means there's no active user
        if resp is None:
            return None
            
        # Handle special case where we get a "no active user" error
        if hasattr(resp, "type") and resp.type == "chatCmdError":
            # Check if it's specifically the "no active user" error
            if (
                hasattr(resp, "chatError") 
                and resp.chatError.get("type") == "error"
                and resp.chatError.get("errorType", {}).get("type") == "noActiveUser"
            ):
                return None
        
        # If we got back a proper ActiveUserResponse, return it
        if isinstance(resp, ActiveUserResponse):
            return resp
            
        # If we received some other type, raise an error
        error_msg = f"Failed to get active user: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def create(
        self,
        display_name: str,
        full_name: str = "",
        image: Optional[str] = None,
        same_servers: bool = True,
        past_timestamp: bool = False,
    ) -> CommandResponse:
        """
        Create a new active user profile.

        Args:
            display_name: Display name for the user profile.
            full_name: Full name for the user profile.
            image: Optional base64-encoded image for the profile.
            same_servers: Whether to use the same servers as existing profiles.
            past_timestamp: Whether to use a past timestamp for the profile creation.

        Returns:
            CommandResponse containing the newly created user profile.

        Raises:
            SimplexCommandError: If there was an error creating the user profile.
        """
        profile = Profile(displayName=display_name, fullName=full_name, image=image)

        cmd = CreateActiveUser(
            type="createActiveUser",
            profile=profile,
            sameServers=same_servers,
            pastTimestamp=past_timestamp,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to create active user: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "activeUser"
        if resp.get("type") != "activeUser":
            error_msg = f"Failed to create active user: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp

    async def set_active(
        self, user_id: int, view_pwd: Optional[str] = None
    ) -> CommandResponse:
        """
        Set the active user.

        Args:
            user_id: ID of the user to set as active.
            view_pwd: Optional view password for hidden users.

        Returns:
            CommandResponse containing the activated user profile.

        Raises:
            SimplexCommandError: If there was an error setting the active user.
        """
        cmd = APISetActiveUser(
            type="apiSetActiveUser", userId=user_id, viewPwd=view_pwd
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to set active user: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "activeUser"
        if resp.get("type") != "activeUser":
            error_msg = f"Failed to set active user: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp

    async def create_address(self) -> CommandResponse:
        """
        Create a new contact address for the active user.

        Returns:
            CommandResponse containing the newly created contact address.

        Raises:
            SimplexCommandError: If there was an error creating the address.
        """
        cmd = CreateMyAddress(type="createMyAddress")
        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to create address: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "userContactLinkCreated"
        if resp.get("type") != "userContactLinkCreated":
            error_msg = (
                f"Failed to create address: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp

    async def delete_address(self) -> CommandResponse:
        """
        Delete the contact address for the active user.

        Returns:
            CommandResponse containing the result of the delete operation.

        Raises:
            SimplexCommandError: If there was an error deleting the address.
        """
        cmd = DeleteMyAddress(type="deleteMyAddress")
        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to delete address: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "userContactLinkDeleted"
        if resp.get("type") != "userContactLinkDeleted":
            error_msg = (
                f"Failed to delete address: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp

    async def get_address(self) -> Optional[CommandResponse]:
        """
        Get the current contact address for the active user.

        Returns:
            CommandResponse containing the contact address, or None if not set.

        Raises:
            SimplexCommandError: If there was an error getting the address.
        """
        cmd = ShowMyAddress(type="showMyAddress")
        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to get address: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        if resp.get("type") == "userContactLink":
            # Convert to proper response type
            return UserContactLinkResponse.from_dict(resp)
        elif resp.get("type") == "chatCmdError":
            # Special case for "no user contact link" which is not an error
            error_info = resp.get("chatError", {})
            if (
                error_info.get("type") == "errorStore"
                and error_info.get("storeError", {}).get("type")
                == "userContactLinkNotFound"
            ):
                return None

        logger.error(
            f"Failed to get address: Unexpected response type {resp.get('type')}"
        )
        raise SimplexCommandError("Failed to get address: Unexpected response", resp)

    async def enable_auto_accept(
        self, accept_incognito: bool = False, auto_reply_text: Optional[str] = None
    ) -> CommandResponse:
        """
        Enable automatic acceptance of contact requests.

        Args:
            accept_incognito: Whether to accept incognito requests.
            auto_reply_text: Optional text message to send automatically on acceptance.

        Returns:
            CommandResponse containing the result of the operation.

        Raises:
            SimplexCommandError: If there was an error enabling auto accept.
        """
        auto_reply = None
        if auto_reply_text:
            auto_reply = MCText(type="text", text=auto_reply_text)

        auto_accept = (
            {"acceptIncognito": accept_incognito, "autoReply": auto_reply}
            if auto_reply
            else {"acceptIncognito": accept_incognito}
        )

        cmd = AddressAutoAccept(type="addressAutoAccept", autoAccept=auto_accept)
        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to enable auto accept: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "userContactLinkUpdated"
        if resp.get("type") != "userContactLinkUpdated":
            error_msg = f"Failed to enable auto accept: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp

    async def disable_auto_accept(self) -> CommandResponse:
        """
        Disable automatic acceptance of contact requests.

        Returns:
            CommandResponse containing the result of the operation.

        Raises:
            SimplexCommandError: If there was an error disabling auto accept.
        """
        cmd = AddressAutoAccept(type="addressAutoAccept")
        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to disable auto accept: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type might be "userContactLinkUpdated"
        if resp.get("type") != "userContactLinkUpdated":
            error_msg = f"Failed to disable auto accept: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = (
            CommandResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return chat_response or resp
