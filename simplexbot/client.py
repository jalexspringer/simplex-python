import asyncio
import websockets
import json
from typing import AsyncGenerator, Optional

class ChatClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._recv_task: Optional[asyncio.Task] = None
        self._msg_queue: asyncio.Queue = asyncio.Queue()
        self._connected = False

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        self._connected = True
        self._recv_task = asyncio.create_task(self._recv_loop())

    async def _recv_loop(self):
        assert self.websocket is not None
        try:
            async for message in self.websocket:
                data = self._parse_message(message)
                await self._msg_queue.put(data)
        except websockets.ConnectionClosed:
            self._connected = False

    async def disconnect(self):
        if self.websocket and self._connected:
            await self.websocket.close()
        if self._recv_task:
            await self._recv_task
        self._connected = False

    async def send(self, data):
        if not self.websocket or not self._connected:
            raise RuntimeError("Not connected")
        await self.websocket.send(self._serialize_message(data))

    async def messages(self) -> AsyncGenerator[dict, None]:
        while self._connected:
            msg = await self._msg_queue.get()
            yield msg

    def _parse_message(self, message: str) -> dict:
        # Placeholder: parse JSON message
        try:
            return json.loads(message)
        except Exception:
            return {"raw": message}

    def _serialize_message(self, data) -> str:
        # Placeholder: serialize message to JSON
        return json.dumps(data)