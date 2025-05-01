"""
Transport abstraction for Simplex Python client.

Defines the base Transport class and error types, mirroring the TypeScript transport system.
Queues, async iteration, and abstract methods follow Python 3.13 idioms.
"""

from __future__ import annotations

import abc
import asyncio
import contextlib
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

import websockets

from simplexbot.queue import ABQueue

W = TypeVar("W")  # Write type
R = TypeVar("R")  # Read type


class TransportError(Exception):
    """Raised for transport-related errors (connection, protocol, etc)."""

    pass


class Transport(abc.ABC, Generic[W, R]):
    """Abstract base class for chat transport layers.

    Attributes:
        queue: Bounded async queue for received items.
    """

    queue: ABQueue[R]

    def __init__(self, qsize: int):
        self.queue = ABQueue[R](qsize)

    def __aiter__(self):
        return self

    @abc.abstractmethod
    async def close(self) -> None:
        """Close the transport and underlying resources."""
        ...

    @abc.abstractmethod
    async def write(self, data: W) -> None:
        """Write data to the transport."""
        ...

    async def read(self) -> R:
        """Read an item from the queue (async)."""
        return await self.queue.dequeue()

    async def __anext__(self):
        """Get the next item (async iterator protocol)."""
        return await self.queue.__anext__()


class WSTransport(Transport[bytes | str, bytes | str]):
    """WebSocket-based transport for Simplex chat.

    Attributes:
        ws: The underlying WebSocket connection.
        timeout: Timeout for send operations (seconds).
    """

    ws: websockets.WebSocketClientProtocol
    timeout: float

    def __init__(
        self, ws: websockets.WebSocketClientProtocol, timeout: float, qsize: int
    ):
        super().__init__(qsize)
        self.ws = ws
        self.timeout = timeout
        self._reader_task = asyncio.create_task(self._reader())

    @classmethod
    async def connect(
        cls, url: str, timeout: float = 10.0, qsize: int = 100
    ) -> "WSTransport":
        """Establish a new WebSocket connection and return a transport."""
        ws = await websockets.connect(url)
        return cls(ws, timeout, qsize)

    async def _reader(self):
        try:
            async for msg in self.ws:
                await self.queue.enqueue(msg)
        except websockets.ConnectionClosed:
            pass
        finally:
            await self.queue.close()

    async def close(self) -> None:
        """Close the WebSocket connection and queue."""
        await self.ws.close()
        await self.queue.close()
        self._reader_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._reader_task

    async def write(self, data: bytes | str) -> None:
        """Send data to the WebSocket."""
        try:
            await asyncio.wait_for(self.ws.send(data), timeout=self.timeout)
        except Exception as e:
            raise TransportError(f"WebSocket write failed: {e}") from e


@dataclass(kw_only=True)
class ChatServer:
    """Represents a chat server endpoint."""

    host: str
    port: Optional[str] = None


@dataclass(kw_only=True)
class ChatSrvRequest:
    """Request sent to the chat server."""

    corr_id: str
    cmd: str


@dataclass(kw_only=True)
class ChatSrvResponse:
    """Response received from the chat server."""

    corr_id: Optional[str]
    resp: object  # Replace with ChatResponse when defined


@dataclass(kw_only=True)
class ParsedChatSrvResponse:
    """Parsed response from the chat server."""

    corr_id: Optional[str] = None
    resp: Optional[object] = None  # Replace with Optional[ChatResponse] when defined


class ChatResponseError(Exception):
    """Raised for errors in chat server responses."""

    def __init__(self, message: str, data: Optional[str] = None):
        super().__init__(message)
        self.data = data


class ChatTransport(Transport[object, ChatSrvResponse]):
    """High-level transport abstraction for Simplex chat protocol.

    Wraps a WSTransport and provides protocol-aware send/receive methods.
    """

    def __init__(self, ws_transport: WSTransport, timeout: float, qsize: int):
        super().__init__(qsize)
        self._ws = ws_transport
        self.timeout = timeout

    @classmethod
    async def connect(
        cls, server: ChatServer | str, timeout: float = 10.0, qsize: int = 100
    ) -> "ChatTransport":
        """Establish a connection to the given ChatServer or URL."""
        if isinstance(server, str):
            url = server
        else:
            url = (
                f"ws://{server.host}:{server.port}"
                if server.port
                else f"ws://{server.host}"
            )
        ws = await WSTransport.connect(url, timeout=timeout, qsize=qsize)
        return cls(ws, timeout, qsize)

    async def close(self) -> None:
        await self._ws.close()
        await self.queue.close()

    async def write(self, req) -> None:
        """
        Serialize and send the command envelope as {"corrId": ..., "cmd": ...}, matching the TypeScript client.
        """
        import json
        from dataclasses import asdict, is_dataclass
        from simplexbot.utils import cmd_string

        # Determine correlation ID
        if isinstance(req, dict):
            corr_id = req.get("corr_id") or req.get("corrId")
        else:
            corr_id = getattr(req, "corr_id", None) or getattr(req, "corrId", None)
        if not corr_id:
            import uuid
            corr_id = str(uuid.uuid4())
            if hasattr(req, "corr_id"):
                req.corr_id = corr_id
            elif hasattr(req, "corrId"):
                req.corrId = corr_id

        # Convert dataclass or dict to command dict
        if is_dataclass(req):
            cmd_dict = asdict(req)
        elif isinstance(req, dict):
            cmd_dict = dict(req)
        else:
            raise TypeError(f"Unsupported command type: {type(req)}")

        # Convert to protocol string
        cmd_str = cmd_string(cmd_dict)
        payload = {"corrId": corr_id, "cmd": cmd_str}
        data = json.dumps(payload)
        print(f"[DEBUG] Sending command envelope: {data}")
        await self._ws.write(data)

    async def read(self) -> ChatSrvResponse:
        # Deserialize response as needed (placeholder: JSON string to dict)
        import json

        msg = await self._ws.read()
        print(f"[DEBUG] Received raw message: {msg}")  # Debug print
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8")
        obj = json.loads(msg)
        return ChatSrvResponse(corr_id=obj.get("corrId"), resp=obj.get("resp"))

    async def __anext__(self):
        return await self.read()


async def with_timeout(timeout: float, coro):
    """Run an awaitable with a timeout, raising asyncio.TimeoutError on expiry."""
    return await asyncio.wait_for(coro, timeout=timeout)


async def delay(ms: float = 0):
    """Asynchronous sleep for the given milliseconds (default: 0)."""
    await asyncio.sleep(ms / 1000)
