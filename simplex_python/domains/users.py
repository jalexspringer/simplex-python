"""
Users domain client for the Simplex Chat protocol.
"""

from typing import Any, Optional, TypedDict
import logging

from .base import BaseDomainClient

logger = logging.getLogger(__name__)


class UserProfile(TypedDict, total=False):
    """Type definition for user profile data."""
    
    displayName: str
    fullName: str
    image: str
    preferences: dict[str, Any]


class UsersClient(BaseDomainClient["UsersClient"]):
    """Client for user-related operations."""
    
    async def set_active(self, user_id: int, view_pwd: Optional[str] = None) -> "UsersClient":
        """
        Set the active user for the session.
        
        Args:
            user_id: ID of the user to activate
            view_pwd: Optional view password for encrypted data
            
        Returns:
            Self for method chaining
        """
        logger.debug(f"Setting active user: {user_id}")
        from ..commands.user import APISetActiveUser
        
        cmd = APISetActiveUser(user_id=user_id)
        if view_pwd is not None:
            cmd.view_pwd = view_pwd
            
        await self._client.send_command(cmd)
        return self
    
    async def get_active(self) -> Optional[dict[str, Any]]:
        """
        Get the currently active user.
        
        Returns:
            User profile object or None if no active user
        """
        logger.debug("Getting active user")
        resp = await self._client.send_command({"type": "showActiveUser"})
        
        logger.debug(f"Got response: {resp}")
        logger.debug(f"Response type: {type(resp)}")
        logger.debug(f"Response has attr 'resp': {hasattr(resp, 'resp')}")
        logger.debug(f"Response has attr 'type': {hasattr(resp, 'type')}")
        
        if not resp:
            logger.debug("Response is None or empty")
            return None
            
        # Handle nested response structure - the actual response may be in a 'resp' field
        if hasattr(resp, 'resp'):
            logger.debug("Response has 'resp' attribute")
            actual_resp = resp.resp
            logger.debug(f"Actual response: {actual_resp}")
            logger.debug(f"Actual response type: {type(actual_resp)}")
        else:
            logger.debug("Using response as is")
            actual_resp = resp
        
        # If actual_resp is a dictionary, use get() for safe access
        if isinstance(actual_resp, dict):
            logger.debug("Actual response is a dictionary")
            resp_type = actual_resp.get("type")
            if resp_type == "activeUser":
                logger.debug("Found activeUser type in dictionary")
                return actual_resp.get("user")
        else:
            # Otherwise, try attribute access
            logger.debug("Trying attribute access")
            resp_type = getattr(actual_resp, "type", None)
            logger.debug(f"Response type via getattr: {resp_type}")
            
            if resp_type == "activeUser":
                logger.debug("Found activeUser type via attribute")
                return getattr(actual_resp, "user", None)
            elif resp_type == "chatCmdError":
                logger.debug("Found chatCmdError type")
                error = getattr(actual_resp, "chatError", {})
                error_type = getattr(error, "errorType", {})
                if getattr(error_type, "type", None) == "noActiveUser":
                    logger.debug("No active user error")
                    return None
                    
        logger.debug("Could not extract user from response, calling _process_response")
        # If we got this far, we have a response but couldn't extract the user
        # Fallback to the _process_response method which will raise an appropriate error
        try:
            await self._process_response(
                actual_resp, 
                "activeUser", 
                "Failed to get active user"
            )
        except Exception as e:
            logger.error(f"_process_response raised: {e}")
            raise
            
        return None  # This line will never be reached due to exception in _process_response
    
    async def create(self, display_name: str, full_name: str = None) -> "UsersClient":
        """
        Create a new user profile.
        
        Args:
            display_name: Display name for the user
            full_name: Optional full name for the user
            
        Returns:
            Self for method chaining
        """
        logger.debug(f"Creating user with display name: {display_name}")
        profile: UserProfile = {"displayName": display_name}
        
        if full_name:
            profile["fullName"] = full_name
            
        await self._client.send_command({
            "type": "apiCreateActiveUser",
            "profile": profile
        })
        return self
    
    async def get_address(self) -> str:
        """
        Get the user's contact address.
        
        Returns:
            Contact address string
            
        Raises:
            SimplexCommandError: If the address cannot be retrieved
        """
        logger.debug("Getting user address")
        resp = await self._client.send_command({"type": "showMyAddress"})
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
            
        # Check for valid response type - could be either "userContactLink" or "userContactLinkShown"
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type in ["userContactLink", "userContactLinkShown"]:
                if "contactLink" in actual_resp:
                    contact_link = actual_resp.get("contactLink", {})
                    return contact_link.get("connReqContact", "")
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type in ["userContactLink", "userContactLinkShown"]:
                if hasattr(actual_resp, "contactLink"):
                    contact_link = getattr(actual_resp, "contactLink", {})
                    return getattr(contact_link, "connReqContact", "")
                    
        # If we couldn't extract the link, use process_response which will raise an error
        await self._process_response(
            actual_resp,
            "userContactLink",  # Accept this type instead of "userContactLinkShown"
            "Failed to get user address"
        )
        return ""  # This line won't be reached due to exception in _process_response
    
    async def create_address(self) -> "UsersClient":
        """
        Create a new contact address for the user.
        
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If address creation fails
        """
        logger.debug("Creating user address")
        resp = await self._client.send_command({"type": "createMyAddress"})
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
        
        # Check for valid response type
        valid_response = False
        
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type in ["userContactLink", "userContactLinkCreated"]:
                valid_response = True
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type in ["userContactLink", "userContactLinkCreated"]:
                valid_response = True
                
        if valid_response:
            logger.debug(f"Successfully created address with response type: {resp_type}")
            return self
                
        # If we couldn't validate the response, use process_response which will raise an error
        await self._process_response(
            actual_resp,
            "userContactLink",  # Accept this type instead of "userContactLinkCreated"
            "Failed to create user address"
        )
        return self  # This line won't be reached due to exception in _process_response
        
    async def delete_address(self) -> "UsersClient":
        """
        Delete the user's contact address.
        
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If address deletion fails
        """
        logger.debug("Deleting user address")
        resp = await self._client.send_command({"type": "deleteMyAddress"})
        await self._process_response(
            resp,
            "userContactLinkDeleted",
            "Failed to delete user address"
        )
        return self
        
    async def set_incognito(self, incognito: bool) -> "UsersClient":
        """
        Set the incognito mode for the active user.
        
        Args:
            incognito: Whether to enable incognito mode
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If setting incognito mode fails
        """
        logger.debug(f"Setting incognito mode: {incognito}")
        resp = await self._client.send_command({
            "type": "setIncognito",
            "is_incognito": incognito
        })
        await self._process_response(
            resp,
            "incognitoUpdated",
            f"Failed to set incognito mode to {incognito}"
        )
        return self
        
    async def enable_auto_accept(self, accept_incognito: bool = False, auto_reply: dict[str, Any] = None) -> "UsersClient":
        """
        Enable automatic acceptance of contact requests.
        
        Args:
            accept_incognito: Whether to accept incognito contacts
            auto_reply: Optional automatic reply message
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If enabling auto-accept fails
        """
        logger.debug(f"Enabling auto-accept with accept_incognito={accept_incognito}")
        auto_accept = {"accept_incognito": accept_incognito}
        
        if auto_reply:
            auto_accept["auto_reply"] = auto_reply
            
        resp = await self._client.send_command({
            "type": "addressAutoAccept",
            "auto_accept": auto_accept
        })
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
        
        # Check for valid response type
        valid_response = False
        
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type in ["userContactLink", "userContactLinkUpdated"]:
                valid_response = True
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type in ["userContactLink", "userContactLinkUpdated"]:
                valid_response = True
                
        if valid_response:
            logger.debug(f"Successfully enabled auto-accept with response type: {resp_type}")
            return self
                
        # If we couldn't validate the response, use process_response which will raise an error
        await self._process_response(
            actual_resp,
            "userContactLink",  # Accept this type instead of "userContactLinkUpdated"
            "Failed to enable auto-accept"
        )
        return self
    
    async def disable_auto_accept(self, accept_incognito: bool = False, auto_reply: dict[str, Any] = None) -> "UsersClient":
        """
        Disable automatic acceptance of contact requests.
        
        Args:
            accept_incognito: Whether to accept incognito contacts
            auto_reply: Optional automatic reply message
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If disabling auto-accept fails
        """
        logger.debug("Disabling auto-accept")
        resp = await self._client.send_command({
            "type": "addressAutoAccept",
            "auto_accept": None  # Send null to disable auto-accept
        })
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
        
        # Check for valid response type
        valid_response = False
        
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type in ["userContactLink", "userContactLinkUpdated"]:
                valid_response = True
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type in ["userContactLink", "userContactLinkUpdated"]:
                valid_response = True
                
        if valid_response:
            logger.debug(f"Successfully disabled auto-accept with response type: {resp_type}")
            return self
                
        # If we couldn't validate the response, use process_response which will raise an error
        await self._process_response(
            actual_resp,
            "userContactLink",  # Accept this type instead of "userContactLinkUpdated"
            "Failed to disable auto-accept"
        )
        return self

    async def hide_user(self, user_id: int, view_pwd: str) -> "UsersClient":
        """
        Hide a user profile.
        
        Args:
            user_id: ID of the user to hide
            view_pwd: View password for encrypted data
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If hiding the user fails
        """
        logger.debug(f"Hiding user: {user_id}")
        from ..commands.user import APIHideUser
        
        cmd = APIHideUser(user_id=user_id, view_pwd=view_pwd)
        resp = await self._client.send_command(cmd)
        
        # Process the response to handle errors
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
            
        await self._process_response(
            actual_resp,
            "userHidden",
            f"Failed to hide user {user_id}"
        )
        return self
        
    async def unhide_user(self, user_id: int, view_pwd: str) -> "UsersClient":
        """
        Unhide a user profile.
        
        Args:
            user_id: ID of the user to unhide
            view_pwd: View password for encrypted data
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If unhiding the user fails
        """
        logger.debug(f"Unhiding user: {user_id}")
        from ..commands.user import APIUnhideUser
        
        cmd = APIUnhideUser(user_id=user_id, view_pwd=view_pwd)
        resp = await self._client.send_command(cmd)
        
        # Process the response to handle errors
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
            
        await self._process_response(
            actual_resp,
            "userUnhidden",
            f"Failed to unhide user {user_id}"
        )
        return self
        
    async def list_users(self) -> list[dict[str, Any]]:
        """
        List all users in the database.
        
        Returns:
            List of user profiles
            
        Raises:
            SimplexCommandError: If listing users fails
        """
        logger.debug("Listing users")
        from ..commands.user import ListUsers
        
        cmd = ListUsers()
        resp = await self._client.send_command(cmd)
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
            
        # Extract users from the response
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type == "usersList":
                return actual_resp.get("users", [])
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type == "usersList":
                return getattr(actual_resp, "users", [])
                
        # If we couldn't extract the users, process the response to handle errors
        await self._process_response(
            actual_resp,
            "usersList",
            "Failed to list users"
        )
        return []  # This line won't be reached due to exception in _process_response

    async def delete(self, user_id: int, del_smp_queues: bool = False) -> "UsersClient":
        """
        Delete a user profile.
        
        Args:
            user_id: ID of the user to delete
            del_smp_queues: Whether to delete SMP queues for the user
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If deleting the user fails
        """
        logger.debug(f"Deleting user: {user_id}")
        # Use a slash command since it appears to be more reliable in the current implementation
        cmd = f"/_delete user {user_id}" + (" queues=on" if del_smp_queues else "")
        resp = await self._client.send_command(cmd)
        
        # Handle nested response structure
        if hasattr(resp, 'resp'):
            actual_resp = resp.resp
        else:
            actual_resp = resp
            
        # Check for valid response type
        if isinstance(actual_resp, dict):
            resp_type = actual_resp.get("type")
            if resp_type == "userDeleted":
                return self
        else:
            resp_type = getattr(actual_resp, "type", None)
            if resp_type == "userDeleted":
                return self
                
        # If we couldn't validate the response, use process_response which will raise an error
        await self._process_response(
            actual_resp,
            "userDeleted",
            f"Failed to delete user {user_id}"
        )
        return self
