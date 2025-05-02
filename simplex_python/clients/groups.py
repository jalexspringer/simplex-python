"""
Groups domain client for SimplexClient.

Provides a fluent API for group-related operations.
"""

import logging
from typing import Optional, TYPE_CHECKING
from ..commands import (
    NewGroup,
    APIAddMember,
    APIJoinGroup,
    APIRemoveMember,
    APILeaveGroup,
    APIListMembers,
    APIUpdateGroupProfile,
    APICreateGroupLink,
    APIGroupLinkMemberRole,
    APIDeleteGroupLink,
    APIGetGroupLink,
    APIGroupMemberInfo,
    APIGetGroupMemberCode,
    APIVerifyGroupMember,
    GroupProfile,
    GroupMemberRole,
)
from ..response import ChatResponse
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class GroupsClient:
    """
    Client for group-related operations in SimplexClient.

    This client is accessed via the `groups` property of SimplexClient
    and provides methods for managing groups and their members.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def create(
        self, display_name: str, full_name: str = "", image: Optional[str] = None
    ) -> ChatResponse:
        """
        Create a new group.

        Args:
            display_name: Display name for the group.
            full_name: Full name for the group (can be empty string).
            image: Optional base64-encoded image for the group.

        Returns:
            ChatResponse containing the newly created group info.
        """
        group_profile = GroupProfile(
            displayName=display_name, fullName=full_name, image=image
        )

        cmd = NewGroup(type="newGroup", groupProfile=group_profile)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to create group: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupCreated" or similar
        if resp.get("type") != "groupCreated":
            error_msg = (
                f"Failed to create group: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def add_member(
        self, group_id: int, contact_id: int, role: str = GroupMemberRole.MEMBER
    ) -> ChatResponse:
        """
        Add a member to a group.

        Args:
            group_id: ID of the group.
            contact_id: ID of the contact to add.
            role: Role to assign to the member (member, admin, or owner).

        Returns:
            ChatResponse containing the newly created group member.
        """
        member_role = role
        if isinstance(role, str) and not isinstance(role, GroupMemberRole):
            # Convert string role to enum if needed
            member_role = GroupMemberRole(role.lower())

        cmd = APIAddMember(
            type="apiAddMember",
            groupId=group_id,
            contactId=contact_id,
            memberRole=member_role,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to add member to group: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "sentGroupInvitation" or similar
        if resp.get("type") != "sentGroupInvitation":
            error_msg = f"Failed to add member to group: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def join(self, group_id: int) -> ChatResponse:
        """
        Join a group.

        Args:
            group_id: ID of the group to join.

        Returns:
            ChatResponse containing the group info.
        """
        cmd = APIJoinGroup(type="apiJoinGroup", groupId=group_id)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to join group: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "userAcceptedGroupSent" or similar
        if resp.get("type") != "userAcceptedGroupSent":
            error_msg = (
                f"Failed to join group: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def remove_member(self, group_id: int, member_id: int) -> ChatResponse:
        """
        Remove a member from a group.

        Args:
            group_id: ID of the group.
            member_id: ID of the member to remove.

        Returns:
            ChatResponse containing the removed member info.
        """
        cmd = APIRemoveMember(
            type="apiRemoveMember", groupId=group_id, memberId=member_id
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to remove member from group: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "userDeletedMember" or similar
        if resp.get("type") != "userDeletedMember":
            error_msg = f"Failed to remove member from group: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def leave(self, group_id: int) -> ChatResponse:
        """
        Leave a group.

        Args:
            group_id: ID of the group to leave.

        Returns:
            ChatResponse containing the group info.
        """
        cmd = APILeaveGroup(type="apiLeaveGroup", groupId=group_id)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to leave group: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "leftMemberUser" or similar
        if resp.get("type") != "leftMemberUser":
            error_msg = (
                f"Failed to leave group: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def list_members(self, group_id: int) -> ChatResponse:
        """
        List members of a group.

        Args:
            group_id: ID of the group.

        Returns:
            ChatResponse containing the list of group members.
        """
        cmd = APIListMembers(type="apiListMembers", groupId=group_id)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to list group members: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupMembers" or similar
        if resp.get("type") != "groupMembers":
            error_msg = f"Failed to list group members: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def update(
        self,
        group_id: int,
        display_name: str,
        full_name: str = "",
        image: Optional[str] = None,
    ) -> ChatResponse:
        """
        Update a group profile.

        Args:
            group_id: ID of the group to update.
            display_name: New display name for the group.
            full_name: New full name for the group.
            image: New base64-encoded image for the group.

        Returns:
            ChatResponse containing the updated group info.
        """
        group_profile = GroupProfile(
            displayName=display_name, fullName=full_name, image=image
        )

        cmd = APIUpdateGroupProfile(
            type="apiUpdateGroupProfile", groupId=group_id, groupProfile=group_profile
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to update group profile: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupUpdated" or similar
        if resp.get("type") != "groupUpdated":
            error_msg = f"Failed to update group profile: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def create_link(
        self, group_id: int, role: str = GroupMemberRole.MEMBER
    ) -> ChatResponse:
        """
        Create a group link with a specified member role.

        Args:
            group_id: ID of the group.
            role: Role for users who join via the link (member, admin, or owner).

        Returns:
            ChatResponse containing the group link.
        """
        member_role = role
        if isinstance(role, str) and not isinstance(role, GroupMemberRole):
            # Convert string role to enum if needed
            member_role = GroupMemberRole(role.lower())

        cmd = APICreateGroupLink(
            type="apiCreateGroupLink", groupId=group_id, memberRole=member_role
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to create group link: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupLinkCreated" or similar
        expected_types = ["groupLinkCreated"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to create group link: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def update_link_role(
        self, group_id: int, role: str = GroupMemberRole.MEMBER
    ) -> ChatResponse:
        """
        Update the member role for a group link.

        Args:
            group_id: ID of the group.
            role: New role for users who join via the link.

        Returns:
            ChatResponse containing the updated link info.
        """
        member_role = role
        if isinstance(role, str) and not isinstance(role, GroupMemberRole):
            # Convert string role to enum if needed
            member_role = GroupMemberRole(role.lower())

        cmd = APIGroupLinkMemberRole(
            type="apiGroupLinkMemberRole", groupId=group_id, memberRole=member_role
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to update group link role: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupLinkUpdated" or similar
        expected_types = ["groupLinkUpdated"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to update group link role: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def delete_link(self, group_id: int) -> ChatResponse:
        """
        Delete a group link.

        Args:
            group_id: ID of the group.

        Returns:
            ChatResponse containing the result of the delete operation.
        """
        cmd = APIDeleteGroupLink(type="apiDeleteGroupLink", groupId=group_id)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to delete group link: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupLinkDeleted" or similar
        expected_types = ["groupLinkDeleted"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to delete group link: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_link(self, group_id: int) -> ChatResponse:
        """
        Get a group link.

        Args:
            group_id: ID of the group.

        Returns:
            ChatResponse containing the group link if it exists.
        """
        cmd = APIGetGroupLink(type="apiGetGroupLink", groupId=group_id)

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get group link: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "groupLink" or similar
        expected_types = ["groupLink"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to get group link: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_member_info(self, group_id: int, member_id: int) -> ChatResponse:
        """
        Get information about a group member.

        Args:
            group_id: ID of the group.
            member_id: ID of the member.

        Returns:
            ChatResponse containing the member information, including connection stats.
        """
        cmd = APIGroupMemberInfo(
            type="apiGroupMemberInfo", groupId=group_id, memberId=member_id
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get member info: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response type may be "groupMemberInfo"
        if resp.get("type") != "groupMemberInfo":
            error_msg = f"Failed to get member info: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_verification_code(
        self, group_id: int, member_id: int
    ) -> ChatResponse:
        """
        Get a verification code for a group member.

        Args:
            group_id: ID of the group.
            member_id: ID of the member.

        Returns:
            ChatResponse containing the verification code.
        """
        cmd = APIGetGroupMemberCode(
            type="apiGetGroupMemberCode", groupId=group_id, groupMemberId=member_id
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to get verification code: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response types might include "connectionCode" or similar
        expected_types = ["connectionCode", "memberCode"]
        if resp.get("type") not in expected_types:
            error_msg = f"Failed to get verification code: Unexpected response type {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def verify_member(
        self, group_id: int, member_id: int, connection_code: str
    ) -> ChatResponse:
        """
        Verify a group member using a connection code.

        Args:
            group_id: ID of the group.
            member_id: ID of the member.
            connection_code: Verification code to validate.

        Returns:
            ChatResponse containing the verification result.
        """
        cmd = APIVerifyGroupMember(
            type="apiVerifyGroupMember",
            groupId=group_id,
            groupMemberId=member_id,
            connectionCode=connection_code,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = f"Failed to verify member: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Expected response might be "memberVerified" or similar
        expected_types = ["memberVerified", "verificationResult"]
        if resp.get("type") not in expected_types:
            error_msg = (
                f"Failed to verify member: Unexpected response type {resp.get('type')}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp
