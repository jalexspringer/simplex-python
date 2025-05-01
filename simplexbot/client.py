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
from typing import AsyncGenerator, Optional

from .queue import ABQueue
from .transport import ChatServer, ChatSrvResponse, ChatTransport


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
        self._event_q: Optional[ABQueue[ChatSrvResponse]] = None
        self._pending: dict[str, asyncio.Future] = {}
        self._recv_task: Optional[asyncio.Task] = None
        self._connected = False

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
        self._event_q = ABQueue[ChatSrvResponse](self._qsize)
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
        cmd,
        expect_response: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional["ChatSrvResponse"]:
        """
        Send a command to the chat server and optionally await a response.

        Args:
            cmd: The command dataclass or dict to send (must have 'type').
            expect_response: If True, await and return the response matching the corr_id.
            timeout: Timeout for this request (seconds).
        Returns:
            The response dataclass, or None if not expecting a response.
        Raises:
            SimplexClientError: On timeout or protocol error.
        """
        import uuid

        # Accept dataclass or dict; always ensure a correlation ID
        corr_id = getattr(cmd, "corr_id", None) or getattr(cmd, "corrId", None)
        if not corr_id:
            corr_id = str(uuid.uuid4())
            if hasattr(cmd, "corr_id"):
                cmd.corr_id = corr_id
            elif hasattr(cmd, "corrId"):
                cmd.corrId = corr_id
        # If dict, assign corr_id
        if isinstance(cmd, dict):
            cmd["corr_id"] = corr_id
        if not self._transport:
            raise SimplexClientError("Not connected")
        fut = None
        if expect_response:
            fut = asyncio.get_running_loop().create_future()
            self._pending[corr_id] = fut
        await self._transport.write(cmd)
        if expect_response:
            try:
                resp = await asyncio.wait_for(fut, timeout or self._timeout)
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
                if (
                    hasattr(resp, "corr_id")
                    and resp.corr_id
                    and resp.corr_id in self._pending
                ):
                    fut = self._pending.pop(resp.corr_id)
                    if not fut.done():
                        fut.set_result(resp)
                else:
                    await self._event_q.enqueue(resp)
        except Exception:
            self._connected = False
            # Optionally: log or handle connection errors here

    async def events(self) -> AsyncGenerator[ChatSrvResponse, None]:
        """
        Async generator yielding server events (responses not matched to a request).
        """
        if not self._event_q:
            raise SimplexClientError("Not connected")
        async for event in self._event_q:
            yield event

    @property
    def connected(self) -> bool:
        """Whether the client is currently connected."""
        return self._connected
