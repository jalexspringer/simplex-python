"""
Messages domain client for SimplexClient.

Provides a fluent API for message-related operations.
"""

import logging
from typing import Optional, Dict, List, Any, TYPE_CHECKING, Union
from ..commands import (
    APISendMessage,
    APIUpdateChatItem,
    APIDeleteChatItem,
    APIDeleteMemberChatItem,
    ComposedMessage,
    ChatType,
    DeleteMode,
    MsgContent,
    MCText,
    ChatItemId,
)
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class MessagesClient:
    """
    Client for message-related operations in SimplexClient.

    This client is accessed via the `messages` property of SimplexClient
    and provides methods for sending, updating, and deleting messages.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def send(
        self,
        chat_id: int,
        messages: List[Union[ComposedMessage, str, Dict[str, Any]]],
        chat_type: ChatType = ChatType.DIRECT,
    ) -> List[Dict[str, Any]]:
        """
        Send one or more messages to a chat.

        Args:
            chat_id: ID of the chat to send to.
            messages: List of messages to send. Can be ComposedMessage objects,
                      strings (converted to text messages), or dicts with message content.
            chat_type: Type of chat (direct, group, or contact request).

        Returns:
            List of chat items created for the sent messages.

        Raises:
            SimplexCommandError: If there was an error sending the messages.
        """
        # Convert messages to ComposedMessage objects if needed
        composed_messages = []
        for msg in messages:
            if isinstance(msg, ComposedMessage):
                composed_messages.append(msg)
            elif isinstance(msg, str):
                # Convert string to text message
                text_content = MCText(type="text", text=msg)
                composed_messages.append(ComposedMessage(msgContent=text_content))
            elif isinstance(msg, dict):
                # Convert dict to ComposedMessage
                msg_content = msg.get("msgContent", msg)
                file_path = msg.get("filePath")
                quoted_item_id = msg.get("quotedItemId")
                composed_messages.append(
                    ComposedMessage(
                        msgContent=msg_content,
                        filePath=file_path,
                        quotedItemId=quoted_item_id,
                    )
                )

        cmd = APISendMessage(
            type="apiSendMessage",
            chatType=chat_type,
            chatId=chat_id,
            messages=composed_messages,
        )

        resp = await self._client.send_command(cmd)

        if not resp:
            logger.error("Failed to send messages: Empty response")
            raise SimplexCommandError("Failed to send messages: Empty response", resp)

        if resp.get("type") == "newChatItems":
            return resp.get("chatItems", [])

        logger.error(
            f"Failed to send messages: Unexpected response type {resp.get('type')}"
        )
        raise SimplexCommandError("Failed to send messages: Unexpected response", resp)

    async def send_text(
        self,
        chat_id: int,
        text: str,
        chat_type: ChatType = ChatType.DIRECT,
        quoted_item_id: Optional[ChatItemId] = None,
    ) -> List[Dict[str, Any]]:
        """
        Send a text message to a chat.

        Args:
            chat_id: ID of the chat to send to.
            text: Text content of the message.
            chat_type: Type of chat (direct, group, or contact request).
            quoted_item_id: Optional ID of a message to quote.

        Returns:
            List of chat items created for the sent message.

        Raises:
            SimplexCommandError: If there was an error sending the message.
        """
        text_content = MCText(type="text", text=text)
        message = ComposedMessage(msgContent=text_content, quotedItemId=quoted_item_id)

        return await self.send(chat_id, [message], chat_type)

    async def update(
        self,
        chat_id: int,
        item_id: ChatItemId,
        content: Union[MsgContent, str, Dict[str, Any]],
        chat_type: ChatType = ChatType.DIRECT,
    ) -> Dict[str, Any]:
        """
        Update the content of a chat item.

        Args:
            chat_id: ID of the chat containing the item.
            item_id: ID of the chat item to update.
            content: New content for the chat item. Can be a MsgContent object,
                    a string (converted to text content), or a dict with message content.
            chat_type: Type of chat (direct, group, or contact request).

        Returns:
            The updated chat item.

        Raises:
            SimplexCommandError: If there was an error updating the chat item.
        """
        # Convert content to MsgContent if needed
        msg_content = content
        if isinstance(content, str):
            msg_content = MCText(type="text", text=content)
        elif isinstance(content, dict) and "type" in content:
            # Assume it's already a valid MsgContent-compatible dict
            msg_content = content

        cmd = APIUpdateChatItem(
            type="apiUpdateChatItem",
            chatType=chat_type,
            chatId=chat_id,
            chatItemId=item_id,
            msgContent=msg_content,
        )

        resp = await self._client.send_command(cmd)

        if not resp:
            logger.error("Failed to update chat item: Empty response")
            raise SimplexCommandError(
                "Failed to update chat item: Empty response", resp
            )

        if resp.get("type") == "chatItemUpdated":
            chat_item = resp.get("chatItem", {})
            return chat_item.get("chatItem", {})

        logger.error(
            f"Failed to update chat item: Unexpected response type {resp.get('type')}"
        )
        raise SimplexCommandError(
            "Failed to update chat item: Unexpected response", resp
        )

    async def delete(
        self,
        chat_id: int,
        item_id: ChatItemId,
        delete_mode: DeleteMode = DeleteMode.BROADCAST,
        chat_type: ChatType = ChatType.DIRECT,
    ) -> Optional[Dict[str, Any]]:
        """
        Delete a chat item.

        Args:
            chat_id: ID of the chat containing the item.
            item_id: ID of the chat item to delete.
            delete_mode: Mode of deletion (broadcast or internal).
            chat_type: Type of chat (direct, group, or contact request).

        Returns:
            The replacement chat item after deletion, if any.

        Raises:
            SimplexCommandError: If there was an error deleting the chat item.
        """
        cmd = APIDeleteChatItem(
            type="apiDeleteChatItem",
            chatType=chat_type,
            chatId=chat_id,
            chatItemId=item_id,
            deleteMode=delete_mode,
        )

        resp = await self._client.send_command(cmd)

        if not resp:
            logger.error("Failed to delete chat item: Empty response")
            raise SimplexCommandError(
                "Failed to delete chat item: Empty response", resp
            )

        if resp.get("type") == "chatItemDeleted":
            to_chat_item = resp.get("toChatItem")
            if to_chat_item:
                return to_chat_item.get("chatItem")
            return None

        logger.error(
            f"Failed to delete chat item: Unexpected response type {resp.get('type')}"
        )
        raise SimplexCommandError(
            "Failed to delete chat item: Unexpected response", resp
        )

    async def delete_member_item(
        self, group_id: int, member_id: int, item_id: int
    ) -> None:
        """
        Delete a chat item from a specific group member.

        Args:
            group_id: ID of the group.
            member_id: ID of the group member.
            item_id: ID of the chat item to delete.

        Raises:
            SimplexCommandError: If there was an error deleting the member's chat item.
        """
        cmd = APIDeleteMemberChatItem(
            type="apiDeleteMemberChatItem",
            groupId=group_id,
            groupMemberId=member_id,
            itemId=item_id,
        )

        resp = await self._client.send_command(cmd)

        if not resp:
            logger.error("Failed to delete member chat item: Empty response")
            raise SimplexCommandError(
                "Failed to delete member chat item: Empty response", resp
            )

        # Expected response type may vary, but we should at least get something
        if resp.get("type") == "chatCmdError":
            logger.error(
                f"Failed to delete member chat item: {resp.get('chatError', {})}"
            )
            raise SimplexCommandError("Failed to delete member chat item", resp)
