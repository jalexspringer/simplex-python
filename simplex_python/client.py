"""
Simplex Python Client (Python 3.13+)

A high-level, fully Pythonic client for the Simplex chat protocol with a fluent API design,
leveraging the project's transport, command, response, and queue infrastructure.

Features:
- Domain-specific clients (users, groups, chats, files, database, connections) with strongly-typed methods
- Async context manager support
- Correlation ID tracking for request/response matching
- Clean separation of concerns
"""

import asyncio
import contextlib
import logging
from typing import AsyncGenerator, Optional, TYPE_CHECKING, Any, Dict, Union
from collections import OrderedDict

from .queue import ABQueue
from .commands import SimplexCommand
from .responses import CommandResponse
from .transport import ChatServer, ChatTransport, ChatSrvRequest
from .client_errors import SimplexClientError, SimplexCommandError

if TYPE_CHECKING:
    from .clients.users import UsersClient
    from .clients.groups import GroupsClient
    from .clients.chats import ChatsClient
    from .clients.files import FilesClient
    from .clients.database import DatabaseClient
    from .clients.connections import ConnectionsClient


# Set up logger
logger = logging.getLogger(__name__)


class SimplexClient:
    """
    High-level async client for the Simplex chat protocol with domain-specific clients.

    Example usage:
        async with SimplexClient(server_or_url) as client:
            # User operations
            user = await client.users.get_active()
            # Group operations
            group = await client.groups.create("Project Team")
            # Chat operations
            await client.chats.send_message(456, "Hello, world!")
            # File operations
            await client.files.set_files_folder("/path/to/downloads")
            # Database operations
            await client.database.export_archive("/path/to/backup.simplex")
            # Connection operations
            await client.connections.accept_contact(123)
            # Listen for events
            async for event in client.events():
                handle_event(event)
    """

    def __init__(
        self, server: Union[ChatServer, str], timeout: float = 10.0, qsize: int = 100
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
        self._event_q: Optional[ABQueue[CommandResponse]] = None
        self._pending: OrderedDict[str, asyncio.Future] = OrderedDict()
        self._recv_task: Optional[asyncio.Task] = None
        self._connected = False
        self._client_corr_id = 0  # Sequential ID counter

        # Lazy-loaded domain-specific client instances
        self._users_client = None
        self._groups_client = None
        self._chats_client = None
        self._files_client = None
        self._database_client = None
        self._connections_client = None

    async def __aenter__(self) -> "SimplexClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def connect(self) -> None:
        """Establish a connection to the chat server."""
        if self._connected:
            return

        self._transport = await ChatTransport.connect(
            self._server, timeout=self._timeout, qsize=self._qsize
        )
        self._event_q = ABQueue[CommandResponse](self._qsize)
        self._recv_task = asyncio.create_task(self._recv_loop())
        self._connected = True
        logger.info("Connected to chat server")

    async def disconnect(self) -> None:
        """Disconnect from the chat server and clean up resources."""
        if not self._connected:
            return

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
        cmd: Union[SimplexCommand, Dict[str, Any]],
        expect_response: bool = True,
    ) -> Optional[CommandResponse]:
        """
        Send a command to the chat server and optionally await a response.

        Args:
            cmd: The command object to send (SimplexCommand or compatible dict).
            expect_response: If True, await and return the response matching the corr_id.

        Returns:
            The response data, or None if not expecting a response.

        Raises:
            SimplexClientError: If not connected or timeout waiting for response.
            SimplexCommandError: If the command results in an error response.
        """
        if not self._transport or not self._connected:
            raise SimplexClientError(
                "Not connected to chat server. Use `async with SimplexClient(...)`"
            )

        # Generate sequential numeric ID
        self._client_corr_id += 1
        corr_id = str(self._client_corr_id)
        logger.debug(f"Generated correlation ID: {corr_id}")

        # Create a command string using the command's to_cmd_string method
        if hasattr(cmd, "to_cmd_string"):
            cmd_str = cmd.to_cmd_string()
        else:
            cmd_str = str(cmd)

        logger.debug(f"Sending command: {cmd_str}")

        # Create a ChatSrvRequest with the correlation ID and command string
        request = ChatSrvRequest(corr_id=corr_id, cmd=cmd_str)

        if expect_response:
            fut = asyncio.get_running_loop().create_future()
            self._pending[corr_id] = fut

        await self._transport.write(request)

        if expect_response:
            try:
                resp = await asyncio.wait_for(fut, self._timeout)

                # Check for error responses
                if isinstance(resp, dict) and resp.get("type") == "chatCmdError":
                    error_info = resp.get("chatError", {})
                    error_msg = f"Command error: {error_info.get('type', 'unknown')}"
                    raise SimplexCommandError(error_msg, resp)

                return resp
            except asyncio.TimeoutError:
                error_msg = f"Timeout waiting for response to command: {cmd_str}"
                raise SimplexClientError(error_msg)
            finally:
                self._pending.pop(corr_id, None)

        return None

    async def _recv_loop(self):
        """Background task that processes incoming messages from the transport."""
        assert self._transport is not None and self._event_q is not None
        try:
            async for resp in self._transport:
                # Extract the correlation ID and response data
                resp_corr_id = getattr(resp, "corr_id", None)
                resp_data = getattr(resp, "resp", resp)

                logger.debug(f"Received response with correlation ID: {resp_corr_id}")

                # If response has a correlation ID and matches a pending request
                if resp_corr_id and resp_corr_id in self._pending:
                    fut = self._pending[resp_corr_id]
                    if not fut.done():
                        logger.debug(
                            f"Resolving future for correlation ID: {resp_corr_id}"
                        )
                        fut.set_result(resp_data)
                else:
                    # No matching future found, treat as an event
                    logger.debug("No matching future found, enqueuing as event")
                    await self._event_q.enqueue(resp_data)
        except Exception as e:
            logger.exception(f"Exception in recv_loop: {e}")
            self._connected = False

    async def events(self) -> AsyncGenerator[CommandResponse, None]:
        """
        Async generator yielding server events (responses not matched to a request).

        Usage:
            async for event in client.events():
                # Process event
        """
        if not self._event_q or not self._connected:
            raise SimplexClientError("Not connected to chat server")

        while self._connected:
            try:
                evt = await self._event_q.dequeue()
                if evt:
                    yield evt
            except Exception as e:
                logger.error(f"Error in events generator: {e}")
                if not self._connected:
                    break

    @property
    def connected(self) -> bool:
        """Whether the client is currently connected."""
        return self._connected

    @property
    def users(self) -> "UsersClient":
        """Access user-related operations with a fluent API."""
        if self._users_client is None:
            from .clients.users import UsersClient

            self._users_client = UsersClient(self)
        return self._users_client

    @property
    def groups(self) -> "GroupsClient":
        """Access group-related operations with a fluent API."""
        if self._groups_client is None:
            from .clients.groups import GroupsClient

            self._groups_client = GroupsClient(self)
        return self._groups_client

    @property
    def chats(self) -> "ChatsClient":
        """Access chat-related operations with a fluent API."""
        if self._chats_client is None:
            from .clients.chats import ChatsClient

            self._chats_client = ChatsClient(self)
        return self._chats_client

    @property
    def files(self) -> "FilesClient":
        """Access file-related operations with a fluent API."""
        if self._files_client is None:
            from .clients.files import FilesClient

            self._files_client = FilesClient(self)
        return self._files_client

    @property
    def database(self) -> "DatabaseClient":
        """Access database-related operations with a fluent API."""
        if self._database_client is None:
            from .clients.database import DatabaseClient

            self._database_client = DatabaseClient(self)
        return self._database_client

    @property
    def connections(self) -> "ConnectionsClient":
        """Access connection-related operations with a fluent API."""
        if self._connections_client is None:
            from .clients.connections import ConnectionsClient

            self._connections_client = ConnectionsClient(self)
        return self._connections_client
