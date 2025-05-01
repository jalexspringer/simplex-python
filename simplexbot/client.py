"""
Simplex Python Client (Python 3.13+)

A high-level, fully Pythonic client for the Simplex chat protocol, leveraging the project's transport, command, response, and queue infrastructure.

Features:
- Strongly-typed, async API for connecting, sending commands, and receiving responses/events.
- Uses ChatTransport, ABQueue, and dataclasses for protocol logic.
- Async context manager support.
- Correlation ID tracking for request/response matching.
- Extensible for additional chat features.
"""

import asyncio
import contextlib
import json
from typing import AsyncGenerator, Optional
from collections import OrderedDict
from enum import Enum

from .queue import ABQueue
from .command import ChatCommand, ShowActiveUser
from .response import ChatResponse
from .transport import ChatServer, ChatTransport, ChatSrvRequest
from .utils import cmd_string


class SimplexClientError(Exception):
    """Raised for client-level errors in SimplexClient."""

    pass


class SimplexClient:
    """
    High-level async client for the Simplex chat protocol.

    Example usage:
        async with SimplexClient(server_or_url) as client:
            await client.send_command(...)
            async for event in client.events():
                ...
    """

    def __init__(
        self, server: ChatServer | str, timeout: float = 10.0, qsize: int = 100
    ):
        """
        Args:
            server: ChatServer object or WebSocket URL to connect to.
            timeout: Connection and command timeout in seconds.
            qsize: Max size of the event queue.
        """
        self._server = server
        self._timeout = timeout
        self._qsize = qsize
        self._transport: Optional[ChatTransport] = None
        self._event_q: Optional[ABQueue[ChatResponse]] = None
        self._pending: OrderedDict[str, asyncio.Future] = OrderedDict()
        self._recv_task: Optional[asyncio.Task] = None
        self._connected = False
        self._client_corr_id = 0  # Add sequential ID counter

    async def __aenter__(self) -> "SimplexClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def connect(self) -> None:
        """Establish a connection to the chat server."""
        self._transport = await ChatTransport.connect(
            self._server, timeout=self._timeout, qsize=self._qsize
        )
        self._event_q = ABQueue[ChatResponse](self._qsize)
        self._recv_task = asyncio.create_task(self._recv_loop())
        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from the chat server and clean up resources."""
        self._connected = False
        if self._recv_task:
            self._recv_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._recv_task
        if self._transport:
            await self._transport.close()
        if self._event_q:
            await self._event_q.close()
        self._pending.clear()

    async def send_command(
        self,
        cmd: ChatCommand,
        expect_response: bool = True,
    ) -> Optional[ChatResponse]:
        """
        Send a command to the chat server and optionally await a response.

        Args:
            cmd: The command dataclass or dict to send (must be a ChatCommand).
            expect_response: If True, await and return the response matching the corr_id.

        Returns:
            The response dataclass, or None if not expecting a response.
        """
        if not self._transport:
            # Throw error because transport should be ready at this point
            raise SimplexClientError(
                "Not connected to chat server. Use `async with SimplexClient(...)`"
            )

        # Generate sequential numeric ID - matching TypeScript implementation
        self._client_corr_id += 1
        corr_id = str(self._client_corr_id)
        print(f"[DEBUG] Generated correlation ID: {corr_id}")
        
        # Create a command string based on the command type
        if isinstance(cmd, dict):
            # For dictionary commands, convert to JSON directly
            cmd_type = cmd.get("type", "")
            if cmd_type == "showActiveUser":
                cmd_str = "/u"
            elif cmd_type == "showUserContactLink":
                user_id = cmd.get("userId", 0)
                cmd_str = f"/_show_address {user_id}"
            elif cmd_type == "createUserContactLink":
                user_id = cmd.get("userId", 0)
                cmd_str = f"/_create_address {user_id}"
            elif cmd_type == "addressAutoAccept":
                # Format for the addressAutoAccept command
                auto_accept = cmd.get("autoAccept", {})
                cmd_str = f"/set_contact_link_mode auto-accept {json.dumps(auto_accept)}"
            elif cmd_type == "apiSendMessage":
                # Convert the chatType to string if it's an enum
                if "chatType" in cmd and hasattr(cmd["chatType"], "value"):
                    cmd["chatType"] = cmd["chatType"].value
                
                # Format as slash command similar to TypeScript implementation
                chat_type = cmd.get("chatType", "@")
                chat_id = cmd.get("chatId", 0)
                messages = cmd.get("messages", [])
                
                # Use the correct command format - matching TypeScript implementation precisely
                msg_json = json.dumps(messages)
                cmd_str = f"/_send {chat_type}{chat_id} json {msg_json}"
            else:
                # Fall back to JSON string for unknown commands
                cmd_str = json.dumps(cmd)
        else:
            # For dataclass commands, use the cmd_string function
            cmd_str = cmd_string(cmd)
        
        # Create a ChatSrvRequest with the correlation ID and command string
        request = ChatSrvRequest(corr_id=corr_id, cmd=cmd_str)

        if expect_response:
            fut = asyncio.get_running_loop().create_future()
            self._pending[corr_id] = fut
            print(f"[DEBUG] Waiting for correlation ID: {corr_id}")
            print(f"[DEBUG] Pending correlation IDs: {list(self._pending.keys())}")

        await self._transport.write(request)
        if expect_response:
            try:
                resp = await asyncio.wait_for(fut, self._timeout)
                return resp
            except asyncio.TimeoutError:
                raise SimplexClientError(f"Timeout waiting for response to {corr_id}")
            finally:
                self._pending.pop(corr_id, None)
        return None

    async def _recv_loop(self):
        assert self._transport is not None and self._event_q is not None
        try:
            async for resp in self._transport:
                # Extract the correlation ID using consistent naming
                resp_corr_id = getattr(resp, "corr_id", None)
                print(f"[DEBUG] Received response with correlation ID: {resp_corr_id}")
                print(f"[DEBUG] Current pending correlation IDs: {list(self._pending.keys())}")
                
                # If response has a correlation ID and it matches a pending request
                if resp_corr_id and resp_corr_id in self._pending:
                    fut = self._pending.pop(resp_corr_id)
                    if not fut.done():
                        print(f"[DEBUG] Resolving future for correlation ID: {resp_corr_id}")
                        # Access the response data - may be direct or in .resp attribute
                        response_data = resp.resp if hasattr(resp, "resp") else resp
                        fut.set_result(response_data)  # Return the actual response data
                else:
                    # No matching future found, treat as an event
                    print("[DEBUG] No matching future found, enqueueing as event")
                    # If resp has a .resp attribute, that's the actual ChatResponse
                    if hasattr(resp, "resp"):
                        await self._event_q.enqueue(resp.resp)
                    else:
                        await self._event_q.enqueue(resp)
        except Exception as e:
            print(f"[DEBUG] Exception in recv_loop: {e}")
            self._connected = False
            # Optionally: log or handle connection errors here

    async def events(self) -> AsyncGenerator[ChatResponse, None]:
        """
        Async generator yielding server events (responses not matched to a request).
        """
        assert self._event_q is not None
        while self._connected:
            try:
                evt = await self.dequeue()
                if evt:
                    yield evt
            except Exception:
                # Log error or handle exception
                print("Error in events generator")

    async def dequeue(self):
        """Dequeue the next event/response from the event queue (TypeScript ABQueue style)."""
        if not self._event_q:
            raise SimplexClientError("Not connected")
        return await self._event_q.dequeue()

    async def get_active_user(self) -> Optional[object]:
        """
        Retrieve the currently active user profile.

        Returns:
            A user profile object (dataclass or dict), or None if no active user exists.

        Raises:
            SimplexClientError: If an unexpected or error response is received.
        """
        resp = await self.send_command(ShowActiveUser(), expect_response=True)
        if not resp:
            return None
        
        # Handle the response - which might be a dict or ChatSrvResponse object
        if hasattr(resp, "resp"):
            r = resp.resp  # ChatSrvResponse object
        else:
            r = resp  # Direct dict access
            
        # Case 1: direct active user response
        if (isinstance(r, dict) and r.get("type") == "activeUser") or (hasattr(r, "type") and getattr(r, "type") == "activeUser"):
            return r["user"] if isinstance(r, dict) else r.user
        # Case 2: contactSubSummary or userContactSubSummary with user info
        if (isinstance(r, dict) and r.get("type") in {"contactSubSummary", "userContactSubSummary"} and "user" in r):
            return r["user"]
        if hasattr(r, "type") and getattr(r, "type") in {"contactSubSummary", "userContactSubSummary"} and hasattr(r, "user"):
            return r.user
        # Case 3: error or no active user
        if (isinstance(r, dict) and r.get("type") == "chatCmdError" and r.get("chatError", {}).get("errorType", {}).get("type") == "noActiveUser"):
            return None
        # Otherwise, unexpected
        raise SimplexClientError(f"Unexpected response to ShowActiveUser: {r!r}")

    async def get_user_address(self) -> Optional[str]:
        """
        Get the user's contact address.
        
        Returns:
            The contact address string or None if not available
        """
        user = await self.get_active_user()
        if not user:
            return None
            
        user_id = user["userId"] if isinstance(user, dict) else user.user_id
        
        # Send the show address command
        resp = await self.send_command({
            "type": "showUserContactLink",
            "userId": user_id
        }, expect_response=True)
        
        if not resp:
            return None
            
        # Handle both dict and object responses
        if isinstance(resp, dict):
            if "contactLink" in resp and "connReqContact" in resp["contactLink"]:
                return resp["contactLink"]["connReqContact"]
        elif hasattr(resp, "contactLink") and hasattr(resp.contactLink, "connReqContact"):
            return resp.contactLink.connReqContact
            
        return None
        
    async def create_user_address(self) -> Optional[str]:
        """
        Create a new user contact address.
        
        Returns:
            The newly created contact address string or None if creation failed
        """
        user = await self.get_active_user()
        if not user:
            return None
            
        user_id = user["userId"] if isinstance(user, dict) else user.user_id
        
        # Send the create address command
        resp = await self.send_command({
            "type": "createUserContactLink",
            "userId": user_id
        }, expect_response=True)
        
        if not resp:
            return None
            
        # Handle both dict and object responses
        if isinstance(resp, dict):
            if "contactLink" in resp and "connReqContact" in resp["contactLink"]:
                return resp["contactLink"]["connReqContact"]
        elif hasattr(resp, "contactLink") and hasattr(resp.contactLink, "connReqContact"):
            return resp.contactLink.connReqContact
            
        return None
        
    async def enable_address_auto_accept(self, accept_incognito: bool = False) -> bool:
        """
        Enable automatic acceptance of incoming contact requests.
        
        Args:
            accept_incognito: Whether to accept incognito contact requests
            
        Returns:
            True if successful, False otherwise
        """
        # Send the auto-accept command matching the TypeScript implementation format
        resp = await self.send_command({
            "type": "addressAutoAccept", 
            "autoAccept": {
                "acceptIncognito": accept_incognito
            }
        }, expect_response=True)
        
        return resp is not None

    async def send_text_message(self, chat_type: Enum, chat_id: int, text: str) -> bool:
        """
        Send a text message to a chat.
        
        Args:
            chat_type: The type of chat (direct, group, etc.)
            chat_id: The ID of the chat
            text: The text message to send
            
        Returns:
            True if successful, False otherwise
        """
        # Convert enum to its string value if it's an Enum
        chat_type_str = chat_type.value if hasattr(chat_type, "value") else chat_type
        
        # Send the text message command
        resp = await self.send_command({
            "type": "apiSendMessage",
            "chatType": chat_type_str,  # Use string value of enum
            "chatId": chat_id,
            "messages": [
                {
                    "msgContent": {
                        "type": "text",
                        "text": text
                    }
                }
            ]
        }, expect_response=True)
        
        return resp is not None

    @property
    def connected(self) -> bool:
        """Whether the client is currently connected."""
        return self._connected

    def _prep_command(self, cmd):
        """Prepare command for transport layer."""
        # If it's a dict, convert appropriate items to strings for the transport
        if isinstance(cmd, dict) and "type" in cmd:
            cmd_type = cmd["type"]
            if cmd_type == "showActiveUser":
                return "/u"
            elif cmd_type == "showMyAddress":
                return "/show_address"
            elif cmd_type == "addressAutoAccept":
                auto_accept = cmd.get("autoAccept", {})
                accept_incognito = auto_accept.get("acceptIncognito", False)
                # Use the accept_incognito variable in the string
                return "/auto_accept on" + (" -i" if accept_incognito else "")
            elif cmd_type == "createMyAddress":
                return "/create_address"
            elif cmd_type == "sendMessage" or cmd_type == "apiSendMessage":
                # Handle message sending commands
                chat_id = cmd.get("chatId", 0)
                messages = cmd.get("messages", [])
                if messages and len(messages) > 0:
                    msg = messages[0]
                    msg_content = msg.get("msgContent", {})
                    if msg_content.get("type") == "text":
                        text = msg_content.get("text", "")
                        return f"/m {chat_id} {text}"
                # Fallback to JSON for complex message commands
                return json.dumps(cmd)
            # Add more command mappings as needed
        
        # For complete commands, convert to JSON string
        if isinstance(cmd, dict):
            return json.dumps(cmd)
        # For command objects, convert to dict then to JSON string
        elif hasattr(cmd, "to_dict"):
            return json.dumps(cmd.to_dict())
        # Return the command as is if already string or other format
        return cmd
