"""
Users domain client for SimplexClient.

Provides a fluent API for user-related operations.
"""

import logging
from typing import Optional, TYPE_CHECKING, Union, Dict, Any

from simplex_python.responses import (
    ActiveUserResponse,
    UsersListResponse,
    UserProfileUpdatedResponse,
    UserProfileNoChangeResponse,
    CommandResponse,
)
from simplex_python.responses.base import StoreErrorType, CmdOkResponse
from ..commands import (
    ShowActiveUser,
    ListUsers,
    APISetActiveUser,
    CreateActiveUser,
    Profile,
    SetProfileAddress,
    CreateMyAddress,
    APIDeleteUser,  # Import the new command
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

    async def get_active(
        self, include_contact_link: bool = True
    ) -> Optional[ActiveUserResponse]:
        """
        Get the currently active user profile.

        Args:
            include_contact_link: Whether to check and include the user's contact link if it exists (default: True)

        Returns:
            ActiveUserResponse containing the user profile object, or None if no active user exists.
            If include_contact_link is True and the user has a contact link, it will be included in the response.

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

        # If we got back a proper ActiveUserResponse, process it
        if isinstance(resp, ActiveUserResponse):
            # If requested, try to get the contact link for the user
            if include_contact_link and "contactLink" not in resp.profile:
                try:
                    # Check if the user has a contact link
                    from ..commands.users import ShowMyAddress

                    address_resp = await self._client.send_command(
                        ShowMyAddress(type="showMyAddress")
                    )

                    # Extract the contact link - could be in different formats
                    contact_link = None
                    if hasattr(address_resp, "contactLink"):
                        if isinstance(address_resp.contactLink, str):
                            contact_link = address_resp.contactLink
                        elif (
                            isinstance(address_resp.contactLink, dict)
                            and "connLinkContact" in address_resp.contactLink
                        ):
                            # Extract from nested dictionary
                            if "connFullLink" in address_resp.contactLink.get(
                                "connLinkContact", {}
                            ):
                                contact_link = address_resp.contactLink[
                                    "connLinkContact"
                                ]["connFullLink"]

                    # Only update if we found a valid link
                    if contact_link:
                        # Update the profile to include the contact link
                        resp.profile["contactLink"] = contact_link
                        # Also update the original user data for backward compatibility
                        if "profile" in resp.user:
                            resp.user["profile"]["contactLink"] = contact_link
                except Exception as e:
                    # Don't fail the whole operation if we can't get the contact link
                    logger.debug(f"Failed to get contact link for active user: {e}")

            return resp

        # If we received some other type, raise an error
        error_msg = f"Failed to get active user: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def list_users(
        self, include_contact_links: bool = False
    ) -> UsersListResponse:
        """
        List all users in the SimpleX Chat system.

        This method retrieves information about all users configured in the
        system, including their profiles, unread counts, and active status.

        Args:
            include_contact_links: Whether to fetch and include contact links for each user (default: False).
                                  Note that enabling this option will switch to each user to fetch their contact link,
                                  which could be slower with many users.

        Returns:
            UsersListResponse containing a list of user items with detailed information.
            The response is iterable and supports indexing to access individual UserItem objects.
            If include_contact_links is True, each user's profile will include their contact link if available.

        Example:
            ```python
            # Get all users without contact links (faster)
            users = await client.users.list_users()

            # Get all users with their contact links (slower but more complete)
            users_with_links = await client.users.list_users(include_contact_links=True)

            # Print number of users
            print(f"Found {len(users)} users")

            # Iterate through users
            for user in users:
                print(f"User: {user.display_name} (ID: {user.user_id})")
                print(f"Active: {user.active_user}")
                print(f"Unread messages: {user.unread_count}")
                if 'contactLink' in user.profile:
                    print(f"Contact Link: {user.profile.get('contactLink')}")

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

        # If we got back a proper UsersListResponse, process it
        if isinstance(resp, UsersListResponse):
            # If requested, fetch contact links for each user
            if include_contact_links:
                # Remember the current active user ID to restore later
                current_active = await self.get_active(include_contact_link=False)
                current_active_id = current_active.user_id if current_active else None

                try:
                    # Import here to avoid circular imports
                    from ..commands.users import ShowMyAddress

                    # For each user in the list, switch to them and get their contact link
                    for user_item in resp:
                        if user_item.user_id == current_active_id:
                            # For the already active user, we can just get their contact link directly
                            try:
                                address_resp = await self._client.send_command(
                                    ShowMyAddress(type="showMyAddress")
                                )
                                # Extract the contact link - could be in different formats
                                contact_link = None
                                if hasattr(address_resp, "contactLink"):
                                    if isinstance(address_resp.contactLink, str):
                                        contact_link = address_resp.contactLink
                                    elif (
                                        isinstance(address_resp.contactLink, dict)
                                        and "connLinkContact"
                                        in address_resp.contactLink
                                    ):
                                        # Extract from nested dictionary
                                        if (
                                            "connFullLink"
                                            in address_resp.contactLink.get(
                                                "connLinkContact", {}
                                            )
                                        ):
                                            contact_link = address_resp.contactLink[
                                                "connLinkContact"
                                            ]["connFullLink"]
                                # Only update if we found a valid link
                                if contact_link:
                                    user_item.profile["contactLink"] = contact_link
                                    if "profile" in user_item.user:
                                        user_item.user["profile"]["contactLink"] = (
                                            contact_link
                                        )
                            except Exception as e:
                                logger.debug(
                                    f"Failed to get contact link for active user {user_item.display_name}: {e}"
                                )
                        else:
                            # For other users, we need to switch to them first
                            try:
                                # Switch to this user
                                await self.set_active(user_item.user_id)

                                # Get their contact link
                                address_resp = await self._client.send_command(
                                    ShowMyAddress(type="showMyAddress")
                                )
                                # Extract the contact link - could be in different formats
                                contact_link = None
                                if hasattr(address_resp, "contactLink"):
                                    if isinstance(address_resp.contactLink, str):
                                        contact_link = address_resp.contactLink
                                    elif (
                                        isinstance(address_resp.contactLink, dict)
                                        and "connLinkContact"
                                        in address_resp.contactLink
                                    ):
                                        # Extract from nested dictionary
                                        if (
                                            "connFullLink"
                                            in address_resp.contactLink.get(
                                                "connLinkContact", {}
                                            )
                                        ):
                                            contact_link = address_resp.contactLink[
                                                "connLinkContact"
                                            ]["connFullLink"]
                                # Only update if we found a valid link
                                if contact_link:
                                    user_item.profile["contactLink"] = contact_link
                                    if "profile" in user_item.user:
                                        user_item.user["profile"]["contactLink"] = (
                                            contact_link
                                        )
                            except Exception as e:
                                logger.debug(
                                    f"Failed to get contact link for user {user_item.display_name}: {e}"
                                )

                    # Restore the original active user
                    if current_active_id is not None:
                        await self.set_active(current_active_id)

                except Exception as e:
                    logger.warning(f"Failed to include contact links for users: {e}")
                    # If we switch users but fail, try to restore the original active user
                    if current_active_id is not None:
                        try:
                            await self.set_active(current_active_id)
                        except Exception as restore_error:
                            logger.error(
                                f"Failed to restore original active user: {restore_error}"
                            )

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
        past_timestamp: bool = False,
        create_profile_address: bool = True,
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
            create_profile_address: Whether to automatically create a profile address for the user (default: True)

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
        profile = Profile(displayName=display_name, fullName=full_name)

        # Create the command with the typed profile object
        # The profile is properly serialized by the command formatter
        # using the to_dict method we've defined
        cmd = CreateActiveUser(
            type="createActiveUser",
            profile=profile,
            sameServers=same_servers,
            pastTimestamp=past_timestamp,
        )

        # Send the command
        resp = await self._client.send_command(cmd)
        print(resp)

        # If we got None back, that's unexpected for this command
        if resp is None:
            error_msg = f"Failed to create user {display_name}: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # If we got back a proper ActiveUserResponse, store it
        if not isinstance(resp, ActiveUserResponse):
            # If we received some other type, raise an error
            error_msg = f"Failed to create user {display_name}: Unexpected response type {getattr(resp, 'type', 'unknown')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        user_resp = resp

        # Create profile address if requested
        if create_profile_address:
            try:
                # First, create the contact address
                create_cmd = CreateMyAddress(type="createMyAddress")
                await self._client.send_command(create_cmd)

                # Then, include it in the profile
                await self.set_profile_address(enabled=True)

                logger.info(
                    f"Successfully created profile address for new user {display_name}"
                )
            except SimplexCommandError as e:
                # Log the error but don't fail the whole operation
                logger.warning(
                    f"Failed to create profile address for user {display_name}: {e}"
                )
                # We don't re-raise the exception since the user was created successfully

        return user_resp

    async def set_profile_address(
        self, enabled: bool = True, create_if_missing: bool = True
    ) -> Union[UserProfileUpdatedResponse, UserProfileNoChangeResponse]:
        """
        Enable or disable the contact address in the active user's profile.

        When enabled, this creates a shareable contact address that others can
        use to connect with the user. The address will be included in the user's
        profile and can be shared with others.

        Args:
            enabled: Whether to enable (True) or disable (False) the profile address
            create_if_missing: Whether to create the contact address if it doesn't exist (default: True)

        Returns:
            UserProfileUpdatedResponse containing the updated profile information when there's a change,
            or UserProfileNoChangeResponse when there's no change to be made.

        Example:
            ```python
            # Enable profile address
            profile_update = await client.users.set_profile_address(enabled=True)
            if isinstance(profile_update, UserProfileUpdatedResponse):
                print(f"Profile address enabled: {profile_update.toProfile.get('contactLink')}")

            # Disable profile address
            profile_update = await client.users.set_profile_address(enabled=False)
            if isinstance(profile_update, UserProfileNoChangeResponse):
                print("No change needed to profile address")
            ```

        Raises:
            SimplexCommandError: If there was an error updating the profile
        """
        # Create the command
        cmd = SetProfileAddress(type="setProfileAddress", includeInProfile=enabled)

        # Send the command
        resp = await self._client.send_command(cmd)

        # If we got None back, that's unexpected for this command
        if resp is None:
            action = "enable" if enabled else "disable"
            error_msg = f"Failed to {action} profile address: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # If we got back a proper response, return it
        if isinstance(resp, (UserProfileUpdatedResponse, UserProfileNoChangeResponse)):
            return resp

        # Special handling for store errors when working with profile addresses
        if isinstance(resp, StoreErrorType):
            if enabled:
                # When enabling: Handle both duplicate and not found cases
                if resp.is_duplicate_contact_link_error():
                    logger.info(
                        "Profile address already exists, returning no change response"
                    )
                    return UserProfileNoChangeResponse(type="userProfileNoChange")

                # When 'contact link not found' error happens, it means the user doesn't have one
                # Attempt to create it first if requested
                if resp.is_contact_link_not_found_error() and create_if_missing:
                    try:
                        # First, create the contact address
                        logger.info("Profile address not found, creating one")
                        create_cmd = CreateMyAddress(type="createMyAddress")
                        await self._client.send_command(create_cmd)

                        # Then, try to include it in the profile again
                        logger.info("Retrying profile address inclusion")
                        return await self.set_profile_address(
                            enabled=True, create_if_missing=False
                        )
                    except SimplexCommandError as e:
                        # If we failed to create the address, include that in the error
                        error_msg = f"Failed to create profile address: {e}"
                        logger.error(error_msg)
                        raise SimplexCommandError(error_msg, resp)

                if resp.is_contact_link_not_found_error():
                    error_msg = "Cannot enable profile address: User doesn't have a contact link"
                    logger.info(error_msg)
                    # This is a valid error case, but we choose to create a UserProfileNoChangeResponse
                    # to maintain consistency with how we handle other cases
                    return UserProfileNoChangeResponse(type="userProfileNoChange")
            else:
                # When disabling: We treat 'contact link not found' as a no-change situation
                # (can't disable what doesn't exist)
                if resp.is_contact_link_not_found_error():
                    logger.info(
                        "Profile address doesn't exist, returning no change response"
                    )
                    return UserProfileNoChangeResponse(type="userProfileNoChange")

        # If we received some other type, raise an error
        action = "enable" if enabled else "disable"
        error_msg = f"Failed to {action} profile address: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def delete_user(
        self,
        user_id: int,
        delete_smp_queues: bool = True,
        view_pwd: Optional[str] = None,
    ) -> Union[ActiveUserResponse, "CmdOkResponse"]:
        """
        Delete a user from the SimpleX Chat system.

        This permanently removes the user account and optionally its associated SMP queues.
        If the user is hidden, the view password must be provided.

        IMPORTANT: You cannot delete the currently active user. You must first switch to another
        user with set_active() before deleting a user. Attempting to delete the active user
        will result in a SimplexCommandError with 'cantDeleteActiveUser' error.

        Args:
            user_id: The ID of the user to delete
            delete_smp_queues: Whether to delete the user's SMP queues (default: True)
            view_pwd: Optional view password for hidden users

        Returns:
            ActiveUserResponse containing information about the new active user (if deletion caused a switch)
            or CmdOkResponse if the deletion was successful but no user switch occurred

        Example:
            ```python
            # Get current user before deletion to ensure we're not deleting the active user
            active_user = await client.users.get_active()

            # Only proceed if we're attempting to delete a different user
            if active_user.user_id != user_id_to_delete:
                result = await client.users.delete_user(user_id_to_delete)
                if isinstance(result, ActiveUserResponse):
                    print(f"Deleted user, now active user is: {result.display_name}")
                else:
                    print("User deleted successfully")
            else:
                # Switch to another user first
                users = await client.users.list_users()
                for user in users:
                    if user.user_id != active_user.user_id:
                        await client.users.set_active(user.user_id)
                        await client.users.delete_user(user_id_to_delete)
                        break
            ```

        Raises:
            SimplexCommandError: If there was an error executing the command (e.g., user ID is invalid)
                                 or if attempting to delete the currently active user.
        """
        from ..responses.base import CmdOkResponse

        # Check if we're trying to delete the active user - this will fail with an error
        # but we can provide a better error message by checking first
        active_user = await self.get_active(include_contact_link=False)
        if active_user and active_user.user_id == user_id:
            error_msg = f"Cannot delete the active user (ID: {user_id}). Switch to a different user first with set_active()."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Create the command
        cmd = APIDeleteUser(
            type="apiDeleteUser",
            userId=user_id,
            delSMPQueues=delete_smp_queues,
            viewPwd=view_pwd,
        )

        # Send the command
        resp = await self._client.send_command(cmd)

        # If we got None back, that's unexpected for this command
        if resp is None:
            error_msg = f"Failed to delete user {user_id}: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # If we got back a proper ActiveUserResponse or CmdOkResponse, return it
        if isinstance(resp, (ActiveUserResponse, CmdOkResponse)):
            return resp

        # If we received some other type, raise an error
        error_msg = f"Failed to delete user {user_id}: Unexpected response type {getattr(resp, 'type', 'unknown')}"
        logger.error(error_msg)
        raise SimplexCommandError(error_msg, resp)

    async def rename_user(
        self, user_id: int, new_display_name: str, new_full_name: Optional[str] = None
    ) -> ActiveUserResponse:
        """Rename a user by updating their profile.

        Args:
            user_id: The ID of the user to rename
            new_display_name: The new display name
            new_full_name: Optional new full name

        Returns:
            Updated ActiveUserResponse
        """
        # Get current active user to restore afterward
        current_active = await self.get_active()
        try:
            # Switch to the user we want to rename
            await self.set_active(user_id)

            # Get the current user to preserve existing profile settings
            user = await self.get_active()

            # Create an updated profile
            from ..commands import Profile

            profile = Profile(
                displayName=new_display_name,
                fullName=new_full_name if new_full_name else user.full_name,
            )

            # Send the update profile command
            from ..commands import UpdateProfile

            cmd = UpdateProfile(type="updateProfile", profile=profile)
            updated_user = await self._client.send_command(cmd)

            return updated_user
        finally:
            # Switch back to originally active user if different
            if current_active and current_active.user_id != user_id:
                await self.set_active(current_active.user_id)

    async def enable_address_auto_accept(
        self, accept_incognito: bool = True, auto_reply: Optional[Dict[str, Any]] = None
    ) -> "CommandResponse":
        """
        Enable automatic acceptance of connection requests for the active user.

        This allows the client to automatically accept incoming contact requests,
        which is especially useful for bots or automated services.

        Args:
            accept_incognito: Whether to accept requests from incognito contacts (default: True).
            auto_reply: Optional automatic reply message to send when accepting requests.

        Returns:
            CommandResponse containing the result of the operation.

        Raises:
            SimplexCommandError: If there was an error executing the command.
        """
        # Create the autoAccept configuration
        from ..commands.users import AddressAutoAccept

        # Create a dictionary for the autoAccept field
        auto_accept_dict = {
            "acceptIncognito": accept_incognito
        }
        
        # Only add autoReply if it's provided
        if auto_reply:
            auto_accept_dict["autoReply"] = auto_reply

        # Using addressAutoAccept command type (not apiAddressAutoAccept)
        # This matches the JS client implementation
        cmd = AddressAutoAccept(
            type="addressAutoAccept",
            autoAccept=auto_accept_dict
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if resp is None:
            error_msg = "Failed to enable auto-accept: No response"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)
            
        # The expected response type is "userContactLinkUpdated" according to JS implementation
        if hasattr(resp, "type") and resp.type != "userContactLinkUpdated":
            error_msg = f"Failed to enable auto-accept: Unexpected response type {resp.type}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        return resp
