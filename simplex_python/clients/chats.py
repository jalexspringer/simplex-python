"""
Chats domain client for SimplexClient.

Provides a fluent API for chat-related operations.
"""

import logging
from typing import Optional, Any, TYPE_CHECKING
from ..commands import (
    StartChat,
    APIStopChat,
    APIGetChats,
    APIGetChat,
    APIChatRead,
    APIDeleteChat,
    APIClearChat,
    ChatType,
    ChatPagination,
    ItemRange,
)
from ..response import ChatResponse, ApiChatsResponse, ApiChatResponse
from ..errors import SimplexCommandError

if TYPE_CHECKING:
    from ..client import SimplexClient

logger = logging.getLogger(__name__)


class ChatsClient:
    """
    Client for chat-related operations in SimplexClient.

    This client is accessed via the `chats` property of SimplexClient
    and provides methods for managing chats, including starting/stopping,
    retrieving chat information, and clearing/deleting chats.
    """

    def __init__(self, client: "SimplexClient"):
        """
        Args:
            client: The parent SimplexClient instance.
        """
        self._client = client

    async def start(
        self,
        subscribe_connections: bool = False,
        enable_expire_chat_items: bool = False,
        start_xftp_workers: bool = False,
    ) -> ChatResponse:
        """
        Start a chat session.

        Args:
            subscribe_connections: Whether to subscribe to connection events.
            enable_expire_chat_items: Whether to enable expiring chat items.
            start_xftp_workers: Whether to start XFTP workers.

        Returns:
            ChatResponse containing the chat startup information.
        """
        cmd = StartChat(
            type="startChat",
            subscribeConnections=subscribe_connections,
            enableExpireChatItems=enable_expire_chat_items,
            startXFTPWorkers=start_xftp_workers,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to start chat: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Assuming successful response has type "chatStarted"
        if resp.get("type") != "chatStarted":
            error_msg = f"Failed to start chat: {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def stop(self) -> ChatResponse:
        """
        Stop the current chat session.

        Returns:
            ChatResponse containing the stop response data.
        """
        cmd = APIStopChat(type="apiStopChat")

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict):
            error_msg = (
                f"Failed to stop chat: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Assuming successful response has type "chatStopped"
        if resp.get("type") != "chatStopped":
            error_msg = f"Failed to stop chat: {resp.get('type')}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def get_all(
        self, user_id: int, include_pending: bool = False
    ) -> ApiChatsResponse:
        """
        Get a list of all chats for a user.

        Args:
            user_id: The ID of the user whose chats to retrieve.
            include_pending: Whether to include pending connections.

        Returns:
            ApiChatsResponse containing the list of chats.
        """
        cmd = APIGetChats(
            type="apiGetChats",
            userId=user_id,
            pendingConnections=include_pending,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "apiChats":
            error_msg = (
                f"Failed to get chats: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        api_chats_response = (
            ApiChatsResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return api_chats_response or resp

    async def get(
        self,
        chat_type: str,
        chat_id: int,
        count: int = 100,
        from_id: Optional[str] = None,
        search_text: Optional[str] = None,
    ) -> ApiChatResponse:
        """
        Get a specific chat with its messages.

        Args:
            chat_type: Type of chat ('direct', 'group', or 'contactRequest').
            chat_id: ID of the chat to retrieve.
            count: Number of messages to retrieve.
            from_id: ID to start retrieving messages from.
            search_text: Optional text to search for in messages.

        Returns:
            ApiChatResponse containing the chat information with messages.
        """
        # Convert string chat_type to ChatType enum if needed
        chat_type_enum = chat_type
        if isinstance(chat_type, str):
            chat_type_enum = ChatType(chat_type.lower())

        pagination = ChatPagination(count=count, fromId=from_id)

        cmd = APIGetChat(
            type="apiGetChat",
            chatType=chat_type_enum,
            chatId=chat_id,
            pagination=pagination,
            search=search_text,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "apiChat":
            error_msg = (
                f"Failed to get chat: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        api_chat_response = (
            ApiChatResponse.from_dict(resp) if isinstance(resp, dict) else None
        )

        return api_chat_response or resp

    async def mark_as_read(
        self,
        chat_type: str,
        chat_id: int,
        from_item_id: Optional[str] = None,
        to_item_id: Optional[str] = None,
    ) -> ChatResponse:
        """
        Mark a chat or specific messages as read.

        Args:
            chat_type: Type of chat ('direct', 'group', or 'contactRequest').
            chat_id: ID of the chat.
            from_item_id: Optional start of range to mark as read.
            to_item_id: Optional end of range to mark as read.

        Returns:
            ChatResponse containing the read status information.
        """
        # Convert string chat_type to ChatType enum if needed
        chat_type_enum = chat_type
        if isinstance(chat_type, str):
            chat_type_enum = ChatType(chat_type.lower())

        # Create ItemRange if both from_item_id and to_item_id are provided
        item_range = None
        if from_item_id and to_item_id:
            item_range = ItemRange(fromItemId=from_item_id, toItemId=to_item_id)

        cmd = APIChatRead(
            type="apiChatRead",
            chatType=chat_type_enum,
            chatId=chat_id,
            itemRange=item_range,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "chatRead":
            error_msg = f"Failed to mark chat as read: {resp.get('type') if resp else 'No response'}"
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def delete(self, chat_type: str, chat_id: int) -> ChatResponse:
        """
        Delete a chat.

        Args:
            chat_type: Type of chat ('direct', 'group', or 'contactRequest').
            chat_id: ID of the chat to delete.

        Returns:
            ChatResponse containing the deletion information.
        """
        # Convert string chat_type to ChatType enum if needed
        chat_type_enum = chat_type
        if isinstance(chat_type, str):
            chat_type_enum = ChatType(chat_type.lower())

        cmd = APIDeleteChat(
            type="apiDeleteChat",
            chatType=chat_type_enum,
            chatId=chat_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "chatDeleted":
            error_msg = (
                f"Failed to delete chat: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def clear(self, chat_type: str, chat_id: int) -> ChatResponse:
        """
        Clear all messages from a chat.

        Args:
            chat_type: Type of chat ('direct', 'group', or 'contactRequest').
            chat_id: ID of the chat to clear.

        Returns:
            ChatResponse containing the clear operation information.
        """
        # Convert string chat_type to ChatType enum if needed
        chat_type_enum = chat_type
        if isinstance(chat_type, str):
            chat_type_enum = ChatType(chat_type.lower())

        cmd = APIClearChat(
            type="apiClearChat",
            chatType=chat_type_enum,
            chatId=chat_id,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "chatCleared":
            error_msg = (
                f"Failed to clear chat: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to proper response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp

    async def send_message(self, chat_id: int, content: Any) -> ChatResponse:
        """
        Send a message to a chat.

        This is a shorthand method that uses the MessageCommand from a different domain.
        The actual implementation should be in a messages domain client, but is included
        here for convenience.

        Args:
            chat_id: ID of the chat to send the message to.
            content: Message content to send (can be text, image, file, etc).

        Returns:
            ChatResponse containing the sent message information.
        """
        # Import here to avoid circular dependency
        from ..commands import APISendMessage

        # Convert simple text strings to proper message content
        if isinstance(content, str):
            from ..commands import MCText

            content = MCText(type="text", text=content)

        cmd = APISendMessage(
            type="apiSendMessage",
            chatId=chat_id,
            content=content,
        )

        resp = await self._client.send_command(cmd)

        # Check response type
        if not resp or not isinstance(resp, dict) or resp.get("type") != "sentMessage":
            error_msg = (
                f"Failed to send message: {resp.get('type') if resp else 'No response'}"
            )
            logger.error(error_msg)
            raise SimplexCommandError(error_msg, resp)

        # Convert to response type
        chat_response = ChatResponse.from_dict(resp) if isinstance(resp, dict) else None

        return chat_response or resp
