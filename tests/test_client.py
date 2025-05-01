"""
Test suite for simplexbot.client.ChatClient.
Uses pytest and pytest-asyncio. Requires Python 3.13+ and uv for best practices.
"""
import asyncio
import pytest
from simplexbot.client import ChatClient
import websockets

@pytest.mark.asyncio
async def test_connect_send_receive():
    """
    Integration test: ChatClient connects to a local echo websocket server,
    sends a message, and receives the echoed message.
    The echo_server handler MUST accept both websocket and path arguments!
    """
    async def echo_server(websocket, path):  # FIXED: both websocket and path required
        # Best practice: always accept both websocket and path arguments for websockets.serve compatibility
        async for message in websocket:
            await websocket.send(message)

    # Start a test websocket server on a random port
    server = await websockets.serve(echo_server, "localhost", 0)
    port = server.sockets[0].getsockname()[1]
    uri = f"ws://localhost:{port}"

    client = ChatClient(uri)
    await client.connect()
    test_data = {"type": "test", "msg": "hello"}
    await client.send(test_data)
    # Get the first message from the async generator
    msg = await asyncio.wait_for(anext(client.messages()), timeout=2)
    assert msg == test_data
    await client.disconnect()
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_e2e_with_simplex_server():
    """
    End-to-end test: ChatClient connects to the real Simplex server (must be running on ws://localhost:5225).
    Sends a '/u' command and expects a response (protocol-specific, may need adjustment).
    """
    client = ChatClient("ws://localhost:5225")
    await client.connect()
    # Send a raw command string as per the Simplex protocol (e.g. '/u' for user info)
    await client.send("/u")
    # Wait for a response (protocol-specific: may need to parse/validate response)
    msg = await asyncio.wait_for(anext(client.messages()), timeout=5)
    print("Simplex server response:", msg)
    assert msg is not None  # Adjust this assertion as you implement protocol parsing
    await client.disconnect()