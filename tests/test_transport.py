"""
Tests for simplexbot.transport.WSTransport and Transport base class.

Covers construction, async queue, and WebSocket integration (mocked).
"""

import asyncio
import json
import time
import types
from unittest.mock import AsyncMock

import pytest

from simplexbot.transport import (
    ChatResponseError,
    ChatServer,
    ChatSrvRequest,
    ChatSrvResponse,
    ChatTransport,
    ParsedChatSrvResponse,
    TransportError,
    WSTransport,
    delay,
    with_timeout,
)


class DummyWebSocket:
    def __init__(self):
        self.sent = []
        self.closed = False
        self._recv_queue = asyncio.Queue()

    async def send(self, data):
        self.sent.append(data)

    async def close(self):
        self.closed = True

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await asyncio.wait_for(self._recv_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            raise StopAsyncIteration

    # Helper for test
    async def queue_recv(self, msg):
        await self._recv_queue.put(msg)


@pytest.mark.asyncio
async def test_ws_transport_send_and_receive():
    ws = DummyWebSocket()
    transport = WSTransport(ws, timeout=1.0, qsize=10)

    # Simulate receiving a message
    await ws.queue_recv("hello")
    msg = await transport.read()
    assert msg == "hello"

    # Test sending
    await transport.write("outbound")
    assert ws.sent == ["outbound"]

    # Test close
    await transport.close()
    assert ws.closed


@pytest.mark.asyncio
async def test_ws_transport_write_timeout():
    ws = DummyWebSocket()
    ws.send = AsyncMock(side_effect=asyncio.TimeoutError)
    transport = WSTransport(ws, timeout=0.01, qsize=1)
    with pytest.raises(TransportError):
        await transport.write("fail")
    await transport.close()


def test_chat_server():
    s = ChatServer(host="localhost", port="5225")
    assert s.host == "localhost"
    assert s.port == "5225"
    s2 = ChatServer(host="example.com")
    assert s2.port is None


def test_chat_srv_request():
    req = ChatSrvRequest(corr_id="abc123", cmd="ping")
    assert req.corr_id == "abc123"
    assert req.cmd == "ping"


def test_chat_srv_response():
    resp = ChatSrvResponse(corr_id="xyz", resp={"ok": True})
    assert resp.corr_id == "xyz"
    assert resp.resp["ok"]


def test_parsed_chat_srv_response():
    parsed = ParsedChatSrvResponse(corr_id="id42", resp={"msg": "hi"})
    assert parsed.corr_id == "id42"
    assert parsed.resp["msg"] == "hi"
    parsed2 = ParsedChatSrvResponse()
    assert parsed2.corr_id is None
    assert parsed2.resp is None


def test_chat_response_error():
    err = ChatResponseError("fail", data="bad json")
    assert str(err) == "fail"
    assert err.data == "bad json"


@pytest.mark.asyncio
async def test_chat_transport_write_and_read():
    # Dummy WSTransport mock
    class DummyWS:
        def __init__(self):
            self.sent = []
            self.closed = False
            self._recv_queue = asyncio.Queue()

        async def write(self, data):
            self.sent.append(data)

        async def read(self):
            return await self._recv_queue.get()

        async def close(self):
            self.closed = True

    ws = DummyWS()
    ct = ChatTransport(ws, timeout=1.0, qsize=5)
    # Use new-style command dict with 'type' field
    req = {"type": "showActiveUser", "corr_id": "cid"}
    await ct.write(req)
    sent = ws.sent[0]
    sent_obj = json.loads(sent)
    assert sent_obj["corrId"] == "cid"
    assert sent_obj["cmd"] == "/u"
    # Simulate server response
    resp_json = json.dumps({"corrId": "cid", "resp": {"ok": True}})
    await ws._recv_queue.put(resp_json)
    resp = await ct.read()
    assert isinstance(resp, ChatSrvResponse)
    assert resp.corr_id == "cid"
    assert resp.resp["ok"] is True
    await ct.close()
    assert ws.closed


@pytest.mark.asyncio
async def test_chat_transport_connect_url(monkeypatch):
    # Patch WSTransport.connect
    async def fake_ws_connect(url, timeout, qsize):
        ws = types.SimpleNamespace()
        return ws

    monkeypatch.setattr(WSTransport, "connect", fake_ws_connect)
    ct = await ChatTransport.connect("ws://host:1", timeout=2.0, qsize=3)
    assert isinstance(ct, ChatTransport)
    assert ct.timeout == 2.0
    assert ct._ws is not None


@pytest.mark.asyncio
async def test_chat_transport_connect_server(monkeypatch):
    async def fake_ws_connect(url, timeout, qsize):
        ws = types.SimpleNamespace()
        ws.url = url
        return ws

    monkeypatch.setattr(WSTransport, "connect", fake_ws_connect)
    srv = ChatServer(host="h", port="12")
    ct = await ChatTransport.connect(srv, timeout=4.0, qsize=2)
    assert ct._ws.url == "ws://h:12"
    assert ct.timeout == 4.0


@pytest.mark.asyncio
async def test_with_timeout_success():
    async def short_task():
        await asyncio.sleep(0.01)
        return 42

    result = await with_timeout(0.1, short_task())
    assert result == 42


@pytest.mark.asyncio
async def test_with_timeout_timeout():
    async def long_task():
        await asyncio.sleep(0.2)

    with pytest.raises(asyncio.TimeoutError):
        await with_timeout(0.05, long_task())


@pytest.mark.asyncio
async def test_delay_accuracy():
    start = time.perf_counter()
    await delay(50)  # 50 ms
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed >= 45  # allow some scheduling leeway
