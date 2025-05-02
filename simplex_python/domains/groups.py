"""
Groups domain client for the Simplex Chat protocol.
"""

from typing import Any, List, TypedDict, Optional
import logging

from .base import BaseDomainClient
from ..enums import MemberRole

logger = logging.getLogger(__name__)


class GroupProfile(TypedDict, total=False):
    """Type definition for group profile data."""
    
    display_name: str
    full_name: str
    description: str
    image: str


class GroupsClient(BaseDomainClient["GroupsClient"]):
    """Client for group-related operations."""
    
    async def create(self, display_name: str, description: str = None) -> "GroupsClient":
        """
        Create a new group.
        
        Args:
            display_name: Display name for the group
            description: Optional description for the group
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If group creation fails
        """
        logger.debug(f"Creating group with name: {display_name}")
        profile: GroupProfile = {
            "display_name": display_name,
            "full_name": display_name
        }
        
        if description:
            profile["description"] = description
            
        resp = await self._client.send_command({
            "type": "newGroup",
            "group_profile": profile
        })
        await self._process_response(
            resp,
            "groupCreated",
            f"Failed to create group {display_name}"
        )
        return self
    
    async def add_member(self, group_id: int, contact_id: int, role: str | MemberRole = MemberRole.MEMBER) -> "GroupsClient":
        """
        Add a member to a group.
        
        Args:
            group_id: ID of the group
            contact_id: ID of the contact to add
            role: Role for the member (member, admin, owner)
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If adding the member fails
        """
        logger.debug(f"Adding member {contact_id} to group {group_id} with role {role}")
        
        # Convert string role to enum if needed
        if isinstance(role, str):
            member_role = MemberRole.from_str(role).value
        else:
            member_role = role.value
        
        resp = await self._client.send_command({
            "type": "apiAddMember",
            "groupId": group_id,
            "contactId": contact_id,
            "memberRole": member_role
        })
        
        await self._process_response(
            resp,
            "memberAdded",
            f"Failed to add member {contact_id} to group {group_id}"
        )
        return self
    
    async def remove_member(self, group_id: int, member_id: int) -> "GroupsClient":
        """
        Remove a member from a group.
        
        Args:
            group_id: ID of the group
            member_id: ID of the member to remove
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If removing the member fails
        """
        logger.debug(f"Removing member {member_id} from group {group_id}")
        resp = await self._client.send_command({
            "type": "apiRemoveMember",
            "groupId": group_id,
            "memberId": member_id
        })
        
        await self._process_response(
            resp,
            "memberRemoved",
            f"Failed to remove member {member_id} from group {group_id}"
        )
        return self
    
    async def leave(self, group_id: int) -> "GroupsClient":
        """
        Leave a group.
        
        Args:
            group_id: ID of the group to leave
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If leaving the group fails
        """
        logger.debug(f"Leaving group {group_id}")
        resp = await self._client.send_command({
            "type": "apiLeaveGroup",
            "groupId": group_id
        })
        
        await self._process_response(
            resp,
            "leftGroup",
            f"Failed to leave group {group_id}"
        )
        return self
    
    async def list_members(self, group_id: int) -> List[dict[str, Any]]:
        """
        List members of a group.
        
        Args:
            group_id: ID of the group
            
        Returns:
            List of group members
            
        Raises:
            SimplexCommandError: If listing members fails
        """
        logger.debug(f"Listing members of group {group_id}")
        resp = await self._client.send_command({
            "type": "apiListMembers",
            "groupId": group_id
        })
        
        resp = await self._process_response(
            resp,
            "groupMembers",
            f"Failed to list members of group {group_id}"
        )
        
        return getattr(resp, "members", [])
    
    async def update_profile(self, group_id: int, display_name: str, description: Optional[str] = None) -> "GroupsClient":
        """
        Update a group's profile.
        
        Args:
            group_id: ID of the group
            display_name: New display name for the group
            description: Optional new description for the group
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If updating the profile fails
        """
        logger.debug(f"Updating profile for group {group_id}")
        profile: GroupProfile = {
            "display_name": display_name,
            "full_name": display_name
        }
        
        if description:
            profile["description"] = description
            
        resp = await self._client.send_command({
            "type": "apiUpdateGroupProfile",
            "group_id": group_id,
            "group_profile": profile
        })
        
        await self._process_response(
            resp,
            "groupProfileUpdated",
            f"Failed to update profile for group {group_id}"
        )
        return self
    
    async def create_link(self, group_id: int, member_role: str | MemberRole = MemberRole.MEMBER) -> str:
        """
        Create a group link for joining.
        
        Args:
            group_id: ID of the group
            member_role: Role for new members joining via the link
            
        Returns:
            Group link string
            
        Raises:
            SimplexCommandError: If creating the link fails
        """
        logger.debug(f"Creating link for group {group_id}")
        
        # Convert string role to enum if needed
        if isinstance(member_role, str):
            role_value = MemberRole.from_str(member_role).value
        else:
            role_value = member_role.value
        
        resp = await self._client.send_command({
            "type": "apiCreateGroupLink",
            "group_id": group_id,
            "member_role": role_value
        })
        
        resp = await self._process_response(
            resp,
            "groupLinkCreated",
            f"Failed to create link for group {group_id}"
        )
        
        return getattr(resp, "groupLink", "")

    async def join(self, group_link: str) -> "GroupsClient":
        """
        Join a group using a connection link.
        
        Args:
            group_link: Group connection link
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If joining the group fails
        """
        logger.debug(f"Joining group with link: {group_link}")
        resp = await self._client.send_command({
            "type": "apiJoinGroup",
            "groupLink": group_link
        })
        
        await self._process_response(
            resp,
            "sentGroupInvitation",
            "Failed to join group using provided link"
        )
        return self
