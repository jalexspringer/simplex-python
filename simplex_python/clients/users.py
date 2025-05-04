"""
Users domain client for SimplexClient.

Provides a fluent API for user-related operations.
"""

import logging
from typing import Optional, TYPE_CHECKING

from simplex_python.responses import (
    ActiveUserResponse,
    UsersListResponse,
)
from ..commands import (
    ShowActiveUser,
    ListUsers,
    APISetActiveUser,
    CreateActiveUser,
    Profile,
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

    async def list_users(self) -> UsersListResponse:
        """
        List all users in the SimpleX Chat system.

        This method retrieves information about all users configured in the
        system, including their profiles, unread counts, and active status.

        Returns:
            UsersListResponse containing a list of user items with detailed information.
            The response is iterable and supports indexing to access individual UserItem objects.

        Example:
            ```python
            # Get all users
            users = await client.users.list_users()

            # Print number of users
            print(f"Found {len(users)} users")

            # Iterate through users
            for user in users:
                print(f"User: {user.display_name} (ID: {user.user_id})")
                print(f"Active: {user.active_user}")
                print(f"Unread messages: {user.unread_count}")

            # Access by index
            first_user = users[0]
            ```

        Raises:
            SimplexCommandError: If there was an error executing the command.
        """
        cmd = ListUsers(type="listUsers")
        resp = await self._client.send_command(cmd)

        # If we got None back, that's unexpected for this command
        if resp is None:
            error_msg = "Failed to list users: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # If we got back a proper UsersListResponse, return it
        if isinstance(resp, UsersListResponse):
            return resp

        # If we received some other type, raise an error
        error_msg = f"Failed to list users: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def set_active(
        self, user_id: int, view_pwd: Optional[str] = None
    ) -> ActiveUserResponse:
        """
        Set the active user.

        Changes the current active user in the SimpleX Chat system to the user
        with the specified ID. If the user is hidden, the view password must be provided.

        Args:
            user_id: The ID of the user to set as active
            view_pwd: Optional view password for hidden users

        Returns:
            ActiveUserResponse containing information about the newly activated user

        Example:
            ```python
            # Switch to user with ID 2
            active_user = await client.users.set_active(2)
            print(f"Switched to user: {active_user.display_name}")

            # Switch to a hidden user
            active_user = await client.users.set_active(3, view_pwd="password123")
            ```

        Raises:
            SimplexCommandError: If there was an error executing the command or the user ID is invalid
        """
        cmd = APISetActiveUser(
            type="apiSetActiveUser", userId=user_id, viewPwd=view_pwd
        )
        resp = await self._client.send_command(cmd)

        # If we got None back, that's unexpected for this command
        if resp is None:
            error_msg = f"Failed to set active user {user_id}: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # If we got back a proper ActiveUserResponse, return it
        if isinstance(resp, ActiveUserResponse):
            return resp

        # If we received some other type, raise an error
        error_msg = f"Failed to set active user {user_id}: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def create_active_user(
        self, 
        display_name: str, 
        full_name: str, 
        same_servers: bool = True,
        past_timestamp: bool = False
    ) -> ActiveUserResponse:
        """
        Create a new user profile and set it as active.
        
        This method creates a new user with the specified profile information and 
        sets it as the active user. If a user with the specified display name already
        exists, a SimplexCommandError will be raised with a userExists error type.
        
        Args:
            display_name: The display name for the new user
            full_name: The full name for the new user
            same_servers: Whether to use the same servers as existing users (default: True)
            past_timestamp: Whether to use a past timestamp for the user (default: False)
            
        Returns:
            ActiveUserResponse containing information about the newly created user
            
        Example:
            ```python
            try:
                # Create a new user
                new_user = await client.users.create_active_user(
                    display_name="Alice", 
                    full_name="Alice Smith"
                )
                print(f"Created user: {new_user.display_name} (ID: {new_user.user_id})")
            except SimplexCommandError as e:
                if hasattr(e, 'error_type') and e.error_type.get('type') == 'userExists':
                    print(f"User already exists: {e.error_type.get('contactName')}")
                else:
                    raise
            ```
            
        Raises:
            SimplexCommandError: If there was an error creating the user, including if the user already exists
        """
        # Create profile for the new user using our strongly-typed Profile class
        profile = Profile(
            displayName=display_name,
            fullName=full_name
        )
        
        # Create the command with the typed profile object
        # The profile is properly serialized by the command formatter
        # using the to_dict method we've defined
        cmd = CreateActiveUser(
            type="createActiveUser",
            profile=profile,
            sameServers=same_servers,
            pastTimestamp=past_timestamp
        )
        
        # Send the command
        resp = await self._client.send_command(cmd)
        
        # If we got None back, that's unexpected for this command
        if resp is None:
            error_msg = f"Failed to create user {display_name}: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)
            
        # If we got back a proper ActiveUserResponse, return it
        if isinstance(resp, ActiveUserResponse):
            return resp
            
        # If we received some other type, raise an error
        error_msg = f"Failed to create user {display_name}: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)
