"""
Chats domain client for the Simplex Chat protocol.
"""

from typing import Any, TypedDict, List, Optional
import logging

from .base import BaseDomainClient
from ..enums import ChatType, DeleteMode

logger = logging.getLogger(__name__)


class MessageContent(TypedDict, total=False):
    """Type definition for message content."""
    
    type: str
    text: str
    image: dict[str, Any]
    file: dict[str, Any]


class ChatsClient(BaseDomainClient["ChatsClient"]):
    """Client for chat-related operations."""
    
    async def send_message(self, chat_id: int, text: str, chat_type: str | ChatType = "direct") -> "ChatsClient":
        """
        Send a text message to a chat.
        
        Args:
            chat_id: ID of the chat
            text: Text content of the message
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If sending the message fails
        """
        logger.debug(f"Sending message to chat {chat_id}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        resp = await self._client.send_command({
            "type": "apiSendMessage",
            "chat_type": chat_type_value,
            "chat_id": chat_id,
            "messages": [{
                "msg_content": {
                    "type": "text",
                    "text": text
                }
            }]
        })
        
        await self._process_response(
            resp,
            "newChatItems",
            f"Failed to send message to chat {chat_id}"
        )
        
        return self
    
    async def get_chats(self, user_id: int) -> List[dict[str, Any]]:
        """
        Get all chats for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of chat objects
            
        Raises:
            SimplexCommandError: If retrieving chats fails
        """
        logger.debug(f"Getting chats for user {user_id}")
        resp = await self._client.send_command({
            "type": "apiGetChats",
            "userId": user_id
        })
        
        resp = await self._process_response(
            resp,
            "apiChats",
            f"Failed to get chats for user {user_id}"
        )
        
        return getattr(resp, "chats", [])
    
    async def get_chat(
        self, 
        chat_id: int, 
        chat_type: str | ChatType = "direct", 
        count: int = 100, 
        search: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Get a specific chat with messages.
        
        Args:
            chat_id: ID of the chat
            chat_type: Type of chat (direct, group) - default: direct
            count: Number of messages to retrieve
            search: Optional search term to filter messages
            
        Returns:
            Chat object with messages
            
        Raises:
            SimplexCommandError: If retrieving the chat fails
        """
        logger.debug(f"Getting chat {chat_id} with {count} messages")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        cmd = {
            "type": "apiGetChat",
            "chatType": chat_type_value,
            "chatId": chat_id,
            "pagination": {
                "count": count
            }
        }
        
        if search:
            cmd["search"] = search
            
        resp = await self._client.send_command(cmd)
        
        resp = await self._process_response(
            resp,
            "apiChat",
            f"Failed to get chat {chat_id}"
        )
        
        return getattr(resp, "chat", {})
    
    async def update_chat_item(
        self, 
        chat_id: int, 
        item_id: int, 
        text: str, 
        chat_type: str | ChatType = "direct"
    ) -> "ChatsClient":
        """
        Update a chat message.
        
        Args:
            chat_id: ID of the chat
            item_id: ID of the chat item to update
            text: New text content
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If updating the message fails
        """
        logger.debug(f"Updating chat item {item_id} in chat {chat_id}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        resp = await self._client.send_command({
            "type": "apiUpdateChatItem",
            "chatType": chat_type_value,
            "chatId": chat_id,
            "chatItemId": item_id,
            "msgContent": {
                "type": "text",
                "text": text
            }
        })
        
        await self._process_response(
            resp,
            "chatItemUpdated",
            f"Failed to update chat item {item_id} in chat {chat_id}"
        )
        
        return self
    
    async def delete_chat_item(
        self, 
        chat_id: int, 
        item_id: int, 
        delete_mode: str | DeleteMode = DeleteMode.BROADCAST, 
        chat_type: str | ChatType = "direct"
    ) -> "ChatsClient":
        """
        Delete a chat message.
        
        Args:
            chat_id: ID of the chat
            item_id: ID of the chat item to delete
            delete_mode: Mode of deletion (local, broadcast)
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If deleting the message fails
        """
        logger.debug(f"Deleting chat item {item_id} in chat {chat_id} with mode {delete_mode}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
            
        # Convert string delete mode to enum if needed
        if isinstance(delete_mode, str):
            delete_mode_value = delete_mode
        else:
            delete_mode_value = delete_mode.value
        
        resp = await self._client.send_command({
            "type": "apiDeleteChatItem",
            "chatType": chat_type_value,
            "chatId": chat_id,
            "chatItemId": item_id,
            "deleteMode": delete_mode_value
        })
        
        # For backward compatibility, accept either response type
        # The server may respond with either type depending on version and configuration
        # Different response types based on deletion mode: chatItemDeleted or chatItemDeletedNotification
        if resp and hasattr(resp, "type") and resp.type in ["chatItemDeleted", "chatItemDeletedNotification"]:
            logger.debug(f"Received valid delete response: {resp.type}")
            return self
        else:
            await self._process_response(
                resp,
                "chatItemDeleted" if delete_mode_value == "local" else "chatItemDeletedNotification",
                f"Failed to delete chat item {item_id} in chat {chat_id}"
            )
        
        return self
    
    async def clear_chat(self, chat_id: int, chat_type: str | ChatType = "direct") -> "ChatsClient":
        """
        Clear all messages from a chat.
        
        Args:
            chat_id: ID of the chat
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If clearing the chat fails
        """
        logger.debug(f"Clearing chat {chat_id}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        resp = await self._client.send_command({
            "type": "apiClearChat",
            "chatType": chat_type_value,
            "chatId": chat_id
        })
        
        await self._process_response(
            resp,
            "chatCleared",
            f"Failed to clear chat {chat_id}"
        )
        
        return self
    
    async def delete_chat(self, chat_id: int, chat_type: str | ChatType = "direct") -> "ChatsClient":
        """
        Delete a chat.
        
        Args:
            chat_id: ID of the chat
            chat_type: Type of chat (direct, group) - default: direct
            
        Returns:
            Self for method chaining
            
        Raises:
            SimplexCommandError: If deleting the chat fails
        """
        logger.debug(f"Deleting chat {chat_id}")
        
        # Convert string chat type to enum if needed
        if isinstance(chat_type, str):
            chat_type_value = ChatType.from_str(chat_type).value
        else:
            chat_type_value = chat_type.value
        
        resp = await self._client.send_command({
            "type": "apiDeleteChat",
            "chatType": chat_type_value,
            "chatId": chat_id
        })
        
        await self._process_response(
            resp,
            "chatDeleted",
            f"Failed to delete chat {chat_id}"
        )
        
        return self
