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

from simplex_python.account import AccountClient
from simplex_python.responses import DynamicResponse

from .queue import ABQueue
from .transport import ChatServer, ChatTransport, ChatSrvRequest
from .client_errors import (
    SimplexClientError,
    SimplexConnectionError,
)


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
        self._event_q: Optional[ABQueue[DynamicResponse]] = None
        self._pending: OrderedDict[str, asyncio.Future] = OrderedDict()
        self._recv_task: Optional[asyncio.Task] = None
        self._connected = False
        self._client_corr_id = 0  # Sequential ID counter

        # Lazy-loaded domain-specific client instances
        self._users_client = None
        self._account_client = None
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

        try:
            self._transport = await ChatTransport.connect(
                self._server, timeout=self._timeout, qsize=self._qsize
            )
            self._event_q = ABQueue[DynamicResponse](self._qsize)
            self._recv_task = asyncio.create_task(self._recv_loop())
            self._connected = True
            logger.info("Connected to chat server")
        except OSError as e:
            # This is likely a connection error - provide helpful information
            if "Connect call failed" in str(e):
                raise SimplexConnectionError("Connection refused", self._server, e)
            elif "Name or service not known" in str(e):
                raise SimplexConnectionError("Host not found", self._server, e)
            else:
                raise SimplexConnectionError("Connection error", self._server, e)
        except Exception as e:
            # For other errors, still use our custom error but with the original exception
            raise SimplexConnectionError(
                "Unexpected error while connecting", self._server, e
            )

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

    async def send_cmd(self, cmd: str) -> DynamicResponse:
        self._client_corr_id += 1
        corr_id = str(self._client_corr_id)
        request = ChatSrvRequest(corr_id=corr_id, cmd=cmd)
        await self._transport.write(request)
        fut = asyncio.get_running_loop().create_future()
        self._pending[corr_id] = fut
        raw_resp = await asyncio.wait_for(fut, self._timeout)
        response = DynamicResponse.from_dict(raw_resp)
        if len(cmd) > 15:
            cmd = f"{cmd[:15]}..."
        logger.info(f"Command: {cmd}: Response type: {response.res_type}")
        return response

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

    async def events(self) -> AsyncGenerator[DynamicResponse, None]:
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
    def account(self) -> AccountClient:
        if self._account_client is None:
            from .account import AccountClient

            self._account_client = AccountClient(self)
            # Don't call async methods from property getter
        return self._account_client
