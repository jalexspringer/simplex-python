"""
Test suite for simplexbot.client.SimplexClient.
Uses pytest and pytest-asyncio. Requires Python 3.13+ and uv for best practices.
"""

import asyncio

import pytest

from simplexbot.client import SimplexClient, SimplexClientError
from simplexbot.transport import ChatSrvRequest, ChatSrvResponse


class DummyTransport:
    """A dummy ChatTransport for testing SimplexClient logic without a real server."""

    def __init__(self):
        self.sent = []
        self.closed = False
        self.responses = asyncio.Queue()

    async def write(self, cmd):
        self.sent.append(cmd)
        # Simulate echo response with corr_id
        resp = ChatSrvResponse(corr_id=cmd.corr_id, resp={"echo": True})
        await self.responses.put(resp)

    async def close(self):
        self.closed = True

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.closed:
            raise StopAsyncIteration
        return await self.responses.get()


@pytest.mark.asyncio
async def test_simplexclient_send_command(monkeypatch):
    """
    Unit test: SimplexClient sends a command, receives a response, and matches corr_id.
    """

    # Patch ChatTransport.connect to return our dummy
    async def dummy_connect(server, timeout=10.0, qsize=100):
        return DummyTransport()

    monkeypatch.setattr("simplexbot.transport.ChatTransport.connect", dummy_connect)
    client = SimplexClient("dummy://", timeout=0.5)
    await client.connect()
    req = ChatSrvRequest(corr_id=None, cmd="test")
    resp = await client.send_command(req)
    assert resp is not None
    assert resp.corr_id == req.corr_id
    assert resp.resp["echo"] is True
    await client.disconnect()


@pytest.mark.asyncio
async def test_simplexclient_events(monkeypatch):
    """
    Unit test: SimplexClient yields events not matched to corr_id.
    """
    dummy = DummyTransport()

    async def dummy_connect(server, timeout=10.0, qsize=100):
        return dummy

    monkeypatch.setattr("simplexbot.transport.ChatTransport.connect", dummy_connect)
    client = SimplexClient("dummy://", timeout=0.5)
    await client.connect()
    # Simulate an event (no corr_id)
    event = ChatSrvResponse(corr_id=None, resp={"event": True})
    await dummy.responses.put(event)
    gen = client.events()
    result = await asyncio.wait_for(anext(gen), timeout=1)
    assert result.resp["event"] is True
    await client.disconnect()


@pytest.mark.asyncio
async def test_simplexclient_timeout(monkeypatch):
    """
    Unit test: SimplexClient raises on timeout waiting for response.
    """

    class SlowTransport(DummyTransport):
        async def write(self, cmd):
            # Do not enqueue a response
            pass

    async def dummy_connect(server, timeout=10.0, qsize=100):
        return SlowTransport()

    monkeypatch.setattr("simplexbot.transport.ChatTransport.connect", dummy_connect)
    client = SimplexClient("dummy://", timeout=0.1)
    await client.connect()
    req = ChatSrvRequest(corr_id=None, cmd="slow")
    with pytest.raises(SimplexClientError):
        await client.send_command(req)
    await client.disconnect()
