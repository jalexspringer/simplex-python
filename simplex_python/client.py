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
import logging
from typing import AsyncGenerator, Optional, TYPE_CHECKING, Any
from collections import OrderedDict

from .queue import ABQueue
from .utils.command_formatting import cmd_string
from .command import ChatCommand
from .response import ChatResponse
from .transport import ChatServer, ChatTransport, ChatSrvRequest

if TYPE_CHECKING:
    from .domains.users import UsersClient
    from .domains.groups import GroupsClient
    from .domains.chats import ChatsClient
    from .domains.files import FilesClient


# Set up logger
logger = logging.getLogger(__name__)


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

        # Using domain-specific clients
        async with SimplexClient(server_or_url) as client:
            # User operations
            await client.users.set_active(123)
            # Group operations
            await client.groups.create("Project Team")
            # Chat operations
            await client.chats.send_message(456, "Hello, world!")
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

        # Domain-specific client instances
        self._users_client = None
        self._groups_client = None
        self._chats_client = None
        self._files_client = None

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
        logger.info("Connected to chat server")

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
        logger.info("Disconnected from chat server")

    async def send_command(
        self,
        cmd: ChatCommand | dict[str, Any],
        expect_response: bool = True,
    ) -> Optional[ChatResponse]:
        """
        Send a command to the chat server and optionally await a response.

        Args:
            cmd: The command dataclass or dict to send (must be a ChatCommand).
            expect_response: If True, await and return the response matching the corr_id.

        Returns:
            The response dataclass, or None if not expecting a response.

        Raises:
            SimplexClientError: If not connected or timeout waiting for response.
        """
        if not self._transport:
            raise SimplexClientError(
                "Not connected to chat server. Use `async with SimplexClient(...)`"
            )

        # Generate sequential numeric ID
        self._client_corr_id += 1
        corr_id = str(self._client_corr_id)
        logger.debug(f"Generated correlation ID: {corr_id}")

        # Create a command string
        cmd_str = self._prep_command(cmd)

        # Create a ChatSrvRequest with the correlation ID and command string
        request = ChatSrvRequest(corr_id=corr_id, cmd=cmd_str)

        if expect_response:
            fut = asyncio.get_running_loop().create_future()
            self._pending[corr_id] = fut
            logger.debug(f"Waiting for correlation ID: {corr_id}")

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
                # Extract the correlation ID
                resp_corr_id = getattr(resp, "corr_id", None)
                logger.debug(f"Received response with correlation ID: {resp_corr_id}")

                # If response has a correlation ID and matches a pending request
                if resp_corr_id and resp_corr_id in self._pending:
                    fut = self._pending.pop(resp_corr_id)
                    if not fut.done():
                        logger.debug(
                            f"Resolving future for correlation ID: {resp_corr_id}"
                        )
                        # Access the response data
                        response_data = getattr(resp, "resp", resp)
                        fut.set_result(response_data)
                else:
                    # No matching future found, treat as an event
                    logger.debug("No matching future found, enqueueing as event")
                    await self._event_q.enqueue(getattr(resp, "resp", resp))
        except Exception as e:
            logger.exception(f"Exception in recv_loop: {e}")
            self._connected = False

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
            except Exception as e:
                logger.error(f"Error in events generator: {e}")

    async def dequeue(self) -> Optional[ChatResponse]:
        """Dequeue the next event/response from the event queue."""
        if not self._event_q:
            raise SimplexClientError("Not connected")
        return await self._event_q.dequeue()

    async def get_active_user(self) -> Optional[Any]:
        """
        Retrieve the currently active user profile.

        Returns:
            A user profile object, or None if no active user exists.

        Raises:
            SimplexClientError: If an unexpected or error response is received.
        """
        logger.debug("Getting active user")
        # Delegate to users domain client for consistency
        return await self.users.get_active()

    @property
    def connected(self) -> bool:
        """Whether the client is currently connected."""
        return self._connected

    @property
    def users(self) -> "UsersClient":
        """Access user-related operations."""
        if self._users_client is None:
            from .domains.users import UsersClient

            self._users_client = UsersClient(self)
        return self._users_client

    @property
    def groups(self) -> "GroupsClient":
        """Access group-related operations."""
        if self._groups_client is None:
            from .domains.groups import GroupsClient

            self._groups_client = GroupsClient(self)
        return self._groups_client

    @property
    def chats(self) -> "ChatsClient":
        """Access chat-related operations."""
        if self._chats_client is None:
            from .domains.chats import ChatsClient

            self._chats_client = ChatsClient(self)
        return self._chats_client

    @property
    def files(self) -> "FilesClient":
        """Access file-related operations."""
        if self._files_client is None:
            from .domains.files import FilesClient

            self._files_client = FilesClient(self)
        return self._files_client

    def _prep_command(self, cmd: ChatCommand | dict[str, Any]) -> str:
        """Prepare command for transport layer."""
        # Use the centralized cmd_string utility function for all command formatting
        return cmd_string(cmd)
