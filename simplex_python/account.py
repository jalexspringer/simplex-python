import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from simplex_python.client_errors import SimplexClientError
from simplex_python.responses import DynamicResponse

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..client import SimplexClient


class ChatType(str, Enum):
    """Type of chat."""

    DIRECT = "@"
    GROUP = "#"
    CONTACT_REQUEST = "<@"


class AccountClient:
    """Client for managing SimpleX user accounts and messaging.

    This client provides methods for working with user accounts, managing connections,
    and sending/receiving messages in the SimpleX chat network.

    Attributes:
        active_user_id: ID of the currently active user.
        active_user_display: Display name of the currently active user.
        active_user_full_name: Full name of the currently active user.
        active_user_contact_link: Contact link of the currently active user.
        active_user_preferences: User preferences of the currently active user.
        active_user_profile: Profile information of the currently active user.
    """

    def __init__(self, client: "SimplexClient") -> None:
        """Initialize the AccountClient.

        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client
        self.active_user_id: Optional[int] = None
        self.active_user_display: Optional[str] = None
        self.active_user_full_name: Optional[str] = None
        self.active_user_contact_link: Optional[str] = None
        self.active_user_preferences: Optional[Dict[str, Any]] = None
        self.active_user_profile: Optional[Dict[str, Any]] = None

    async def initialize(self, remove_simplex_connections: bool = True) -> None:
        """Initialize the account client by fetching active user data.

        This method should be called after creating the AccountClient instance
        to populate the active user information.
        """
        if self._client.connected:
            await self.active_user()

    async def active_user(self) -> DynamicResponse:
        """Get information about the currently active user.

        Retrieves user details and populates instance attributes with the active user's
        information including ID, display name, full name, and contact link.

        Returns:
            DynamicResponse: Response containing the active user information.
        """
        cmd = "/u"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        if response.res_type == "activeUser":
            res: ActiveUserResponse = ActiveUserResponse(response.raw_response)
            self.active_user_id = res.user_id
            self.active_user_display = res.display_name
            self.active_user_full_name = res.full_name

            # Try to get contact link
            try:
                sa_res = await self._client.send_cmd("/sa")
                self.active_user_contact_link = sa_res.raw_response["contactLink"][
                    "connLinkContact"
                ]["connFullLink"]
            except (KeyError, TypeError, SimplexClientError):
                # Create a new address if one doesn't exist
                await self._client.send_cmd("/address")

                # Get the newly created address
                sa_res = await self._client.send_cmd("/sa")
                self.active_user_contact_link = sa_res.raw_response["contactLink"][
                    "connLinkContact"
                ]["connFullLink"]

            self.active_user_preferences = res.preferences
            self.active_user_profile = res.profile
            return res

        return response

    async def get_active_user_info(self) -> Optional[Dict[str, Any]]:
        """Get active user information in dictionary format.

        Returns:
            Dict[str, Any]: Active user data or None if not available
        """
        response = await self.active_user()
        if hasattr(response, "user"):
            return response.user
        return None

    async def get_onetime_connection_link(self) -> str:
        """Generate a one-time connection link for the current user.

        Creates a new one-time invitation link that can be shared with other users
        to establish a connection.

        Returns:
            str: The full connection link that can be shared.
        """
        cmd: str = "/c"
        response: DynamicResponse = await self._client.send_cmd(cmd)

        return response.raw_response["connLinkInvitation"]["connFullLink"]

    async def connect_with_link(self, conn_link: str) -> Dict[str, Any]:
        """Connect to another user using their connection link.

        Args:
            conn_link: The connection link shared by another user.

        Returns:
            Dict[str, Any]: Information about the new connection.
        """
        cmd = f"/c {conn_link}"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response.raw_response["connection"]

    async def list_connections(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all connections to the current user account, organized by type.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary with keys 'direct' and 'groups',
            each containing a list of corresponding connections.
        """
        direct_connections = await self.list_direct_connections()
        groups = await self.list_groups()

        return {"direct": direct_connections, "groups": groups}

    async def list_direct_connections(self) -> List[Dict[str, Any]]:
        """List all direct connections to the current user account.

        Returns:
            List[Dict[str, Any]]: List of direct connections with each connection having:
                - contact_id: The ID of the contact
                - display_name: The display name of the contact
                - profile_id: The profile ID of the contact
                - full_name: The full name of the contact (if available)
                - unread_count: Number of unread messages
                - unread_chat: Whether the entire chat is unread
                - last_message: Text of the most recent message (if any)
                - last_message_ts: Timestamp of the most recent message (if any)
                - last_message_status: Status information about the last message
                - chat_items: The most recent chat items/messages
                - chat_stats: Statistics about the chat
                - profile: The complete profile information of the contact (without image and contactLink)
        """
        cmd = "/cs"
        response: DynamicResponse = await self._client.send_cmd(cmd)

        # Initialize result structure
        direct_connections = []

        if isinstance(response.data, list):
            for chat in response.data:
                # Skip non-direct chats
                if chat["chatInfo"]["type"] != "direct":
                    continue
                if "SimpleX" in chat["chatInfo"]["contact"]["profile"]["displayName"]:
                    continue

                # Start with essential contact information
                chat_data = {
                    "contact_id": chat["chatInfo"]["contact"]["contactId"],
                    "chat_stats": chat["chatStats"],
                    "chat_items": chat["chatItems"],
                    "unread_count": chat["chatStats"]["unreadCount"],
                    "unread_chat": chat["chatStats"]["unreadChat"],
                }

                # Process profile information
                if "profile" in chat["chatInfo"]["contact"]:
                    profile = chat["chatInfo"]["contact"]["profile"].copy()

                    # Add key profile fields to top level for easier access
                    chat_data["display_name"] = profile.get("displayName", "")
                    chat_data["profile_id"] = profile.get("profileId")
                    chat_data["full_name"] = profile.get("fullName", "")

                    # Remove image and contact link from the profile copy
                    for field in ["image", "contactLink"]:
                        if field in profile:
                            del profile[field]

                    # Keep the complete profile as well
                    chat_data["profile"] = profile

                # Extract the last message information if available
                if chat["chatItems"]:
                    last_item = chat["chatItems"][0]  # Most recent message is first
                    chat_data["last_message"] = last_item["meta"].get("itemText", "")
                    chat_data["last_message_ts"] = last_item["meta"].get("itemTs", "")
                    chat_data["last_message_status"] = last_item["meta"].get(
                        "itemStatus", ""
                    )

                direct_connections.append(chat_data)

        return direct_connections

    async def list_groups(self) -> List[Dict[str, Any]]:
        """List all group chats for the current user account.

        Returns:
            List[Dict[str, Any]]: List of group chats with each group having:
                - group_id: The ID of the group
                - display_name: The display name of the group
                - full_name: The full name of the group (if available)
                - unread_count: Number of unread messages
                - unread_chat: Whether the entire chat is unread
                - unread_mentions: Number of unread mentions
                - last_message: Text of the most recent message (if any)
                - last_message_ts: Timestamp of the most recent message (if any)
                - last_message_status: Status information about the last message
                - chat_items: The most recent chat items/messages
                - chat_stats: Statistics about the chat
                - group_info: The complete group information
        """
        cmd = "/cs"
        response: DynamicResponse = await self._client.send_cmd(cmd)

        # Initialize result structure
        groups = []

        if isinstance(response.data, list):
            for chat in response.data:
                # Skip non-group chats
                if chat["chatInfo"]["type"] != "group":
                    continue

                # Process group chat
                group_info = chat["chatInfo"]["groupInfo"]

                # Create group chat data structure
                chat_data = {
                    "group_id": group_info["groupId"],
                    "chat_stats": chat["chatStats"],
                    "chat_items": chat["chatItems"],
                    "unread_count": chat["chatStats"]["unreadCount"],
                    "unread_chat": chat["chatStats"]["unreadChat"],
                    "unread_mentions": chat["chatStats"].get("unreadMentions", 0),
                    "membership_status": group_info["membership"]["memberStatus"],
                }

                # Add group profile information
                if "groupProfile" in group_info:
                    profile = group_info["groupProfile"]

                    # Add key profile fields to top level for easier access
                    chat_data["display_name"] = profile.get(
                        "displayName", group_info.get("localDisplayName", "")
                    )
                    chat_data["full_name"] = profile.get("fullName", "")

                # Include complete group information
                chat_data["group_info"] = group_info

                # Extract the last message information if available
                if chat["chatItems"]:
                    last_item = chat["chatItems"][0]  # Most recent message is first
                    chat_data["last_message"] = last_item["meta"].get("itemText", "")
                    chat_data["last_message_ts"] = last_item["meta"].get("itemTs", "")
                    chat_data["last_message_status"] = last_item["meta"].get(
                        "itemStatus", ""
                    )

                groups.append(chat_data)

        return groups

    async def get_chat(
        self, user_id: str, chat_type: str = "direct"
    ) -> List[Dict[str, Any]]:
        """Get details for all chat items for a specific user ID.

        Uses the /tail command to retrieve all chat items for a given contact ID.

        Args:
            user_id: The user ID to find chat items for.
            chat_type: Not used with /tail command, kept for compatibility.

        Returns:
            List[Dict[str, Any]]: List of chat items (messages) for the specified user.
                Returns an empty list if no chat items are found.
        """
        cmd = f"/tail {'@' if chat_type == 'direct' else '#'}{user_id}"
        response: DynamicResponse = await self._client.send_cmd(cmd)

        # Extract chat items from the response
        items = []
        if "chatItems" in response.raw_response:
            # Some versions return chat items directly in the response
            for item in response.raw_response["chatItems"]:
                if "chatItem" in item:
                    items.append(item["chatItem"])
                else:
                    items.append(item)

        return items

    async def send_message(
        self, display_name: str, message: str, chat_type: ChatType = ChatType.DIRECT
    ) -> DynamicResponse:
        """Send a message to a user by their display name.

        Args:
            display_name: The display name of the recipient.
            message: The message text to send.

        Returns:
            DynamicResponse: Response containing information about the sent message.
        """

        cmd = f"{chat_type.value}{display_name} {message}"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response

    async def list_users(self) -> List[Dict[str, Any]]:
        """List all users in the local SimpleX database.

        Returns:
            List[Dict[str, Any]]: List of user information.
        """
        cmd = "/users"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response.data

    async def set_active_user(self, user_id: int) -> Dict[str, Any]:
        """Set the active user by user ID.

        Args:
            user_id: The ID of the user to set as active.

        Returns:
            Dict[str, Any]: Response data for the newly activated user.
        """
        cmd = f"/_user {user_id}"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        self.initialize()
        return response.data

    async def create_user(
        self,
        display_name: str,
        full_name: str,
        same_servers: bool = True,
        past_timestamp: bool = False,
        create_profile_address: bool = True,
    ) -> DynamicResponse:
        """Create a new user profile.

        Args:
            display_name: The display name for the new user.
            full_name: The full name for the new user.
            same_servers: Whether to use the same servers as existing users.
            past_timestamp: Whether to use a past timestamp for the user.
            create_profile_address: Whether to automatically create a profile address.

        Returns:
            DynamicResponse: Response containing information about the newly created user.
        """
        profile = Profile(displayName=display_name, fullName=full_name)
        user = {
            "profile": profile.to_dict(),
            "sameServers": same_servers,
            "pastTimestamp": past_timestamp,
        }
        cmd = f"/_create user {json.dumps(user)}"
        try:
            response: DynamicResponse = await self._client.send_cmd(cmd)
        except SimplexClientError as _:
            logger.info(f"ERROR: User {display_name} already exists.")
            return None
        return response

    async def remove_connection(
        self, user_id: int, chat_type: ChatType = ChatType.DIRECT
    ):
        cmd = f"/_delete {chat_type.value}{user_id}"
        try:
            response: DynamicResponse = await self._client.send_cmd(cmd)
        except SimplexClientError as _:
            logger.info(f"No connection with ID {chat_type.value}{user_id} exists.")
            return None
        return response

    async def create_group(
        self, display_name: str, full_name: str = "", image: str = None
    ) -> DynamicResponse:
        """Create a group with display_name and full_name.

        Args:
            display_name: The once word (no spaces) display name of the group
            full name: The full name of the group
            image: link to an image. Not yet implemented

        Returns:
            DynamicResponse: Response containing information about the sent message.
        """

        def to_camel_case(s):
            """
            Convert a space-separated string to camelCase.

            Args:
                s (str): The input string to convert

            Returns:
                str: The camelCase version of the input string
            """
            # If the string is empty or has no spaces, return it as is
            if not s or " " not in s:
                return s

            # Split the string by spaces
            words = s.split()

            # Capitalize all words except the first one
            camel = words[0].lower()
            for word in words[1:]:
                camel += word.capitalize()

            return camel

        cmd = f"/group {to_camel_case(display_name)} {full_name}"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response

    async def add_user_to_group(self, group_display_name: str, user_display_name: str):
        cmd = f"/add {group_display_name} {user_display_name} member"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response

    async def accept_group_invite(self, group_display_name: str):
        cmd = f"/j {group_display_name}"
        response: DynamicResponse = await self._client.send_cmd(cmd)
        return response


@dataclass
class Profile:
    """User profile information.

    Structured representation of a SimpleX user profile, containing
    display name, full name, and optional fields for profile image,
    contact link and profile ID.

    Attributes:
        displayName: User's display name shown in chat lists.
        fullName: User's full name.
        image: Optional base64-encoded profile image.
        contactLink: Optional contact link for the profile.
        profileId: Optional unique identifier for the profile.
    """

    displayName: str
    fullName: str
    image: Optional[str] = None
    contactLink: Optional[str] = None
    profileId: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the profile, with
                optional fields only included when they have values.
        """
        return {
            "displayName": self.displayName,
            "fullName": self.fullName,
            **({"image": self.image} if self.image is not None else {}),
            **(
                {"contactLink": self.contactLink}
                if self.contactLink is not None
                else {}
            ),
            **({"profileId": self.profileId} if self.profileId is not None else {}),
        }


@dataclass
class ActiveUserResponse:
    """Response containing active user information.

    Provides a structured wrapper around the raw response data for the active user,
    with property accessors for commonly used fields.

    Attributes:
        raw_response: The complete raw response dictionary from the server.
    """

    raw_response: Dict[str, Any]

    @property
    def type(self) -> str:
        """Get the response type.

        Returns:
            str: The response type string.
        """
        return self.raw_response.get("type", "")

    @property
    def user(self) -> Dict[str, Any]:
        """Get the complete user data.

        Returns:
            Dict[str, Any]: The complete user information dictionary.
        """
        return self.raw_response.get("user", {})

    @property
    def user_id(self) -> Optional[int]:
        """Get the user ID.

        Returns:
            Optional[int]: The user ID if available.
        """
        return self.user.get("userId")

    @property
    def display_name(self) -> Optional[str]:
        """Get the user's display name.

        Returns:
            Optional[str]: The display name if available.
        """
        return self.user.get("localDisplayName")

    @property
    def full_name(self) -> Optional[str]:
        """Get the user's full name.

        Returns:
            Optional[str]: The full name if available.
        """
        profile = self.user.get("profile", {})
        return profile.get("fullName", "")

    @property
    def profile(self) -> Dict[str, Any]:
        """Get the user's profile information.

        Returns:
            Dict[str, Any]: The profile information dictionary.
        """
        return self.user.get("profile", {})

    @property
    def preferences(self) -> Dict[str, Any]:
        """Get the user's preferences.

        Returns:
            Dict[str, Any]: The preferences dictionary.
        """
        return self.user.get("fullPreferences", {})

    @property
    def contact_link(self) -> Optional[str]:
        """Get the user's contact link.

        Note: Contact link might be in a different location, this is a placeholder.

        Returns:
            Optional[str]: The contact link if available.
        """
        return ""
