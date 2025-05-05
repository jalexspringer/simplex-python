"""
Squaring Bot Example

A simple bot that responds to numbers by calculating their square.
This is an enhanced version that uses all domain-specific clients of the SimplexPython SDK,
demonstrating the Fluent API pattern with proper error handling and type hints.
"""

from pprint import pprint
import asyncio
import logging
import os
from typing import Optional, Dict, Any
from datetime import datetime

from simplex_python.client import SimplexClient
from simplex_python.transport import ChatServer
from simplex_python.responses import CommandResponse
from simplex_python.client_errors import SimplexClientError, SimplexCommandError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configuration constants
SERVER_URL = "ws://localhost:5225"
BOT_DISPLAY_NAME = "SquaringBot"
BOT_FULL_NAME = "Python Squaring Bot"
WELCOME_MSG = "Hello! I am a simple squaring bot - if you send me a number, I will calculate its square"


async def setup_bot(server_address: str) -> SimplexClient:
    """Set up a bot with the given port and display name."""
    client = SimplexClient(server_address)
    await client.connect()

    # Show user info
    await client.account.initialize()

    print(
        f"Connected: {client.account.active_user_display} --- ID: {client.account.active_user_id}"
    )

    return client


async def get_bot_clients():
    # Create two bots on different ports
    print("Setting up Bot 1...")
    SERVER_URL = "ws://localhost:5225"
    bot1 = await setup_bot(SERVER_URL)

    print("Setting up Bot 2...")
    SERVER_URL = "ws://localhost:5226"
    bot2 = await setup_bot(SERVER_URL)

    for b in [bot1, bot2]:
        await b.account.remove_connection(1)
        await b.account.remove_connection(2)
        await b.account.remove_connection(3)

    return bot1, bot2


async def process_events(client: SimplexClient) -> None:
    """Process incoming events from the chat server.

    Args:
        client: The SimplexClient instance
    """
    logger.info("Starting to process events...")

    # Process incoming messages
    async for event in client.events():
        if not isinstance(event, dict):
            continue

        event_type = event.get("type")

        # Handle contact connected event
        if event_type == "contactConnected":
            contact = event.get("contact", {})
            contact_id = contact.get("contactId")
            contact_profile = contact.get("profile", {})
            contact_name = contact_profile.get("displayName", "Unknown")
            logger.info(f"Contact connected: {contact_name} (ID: {contact_id})")

        # Handle new chat items
        elif event_type == "newChatItems":
            pprint(event)

            chat_items = event.get("chatItems", [])

            for item in chat_items:
                # Extract chat info and item content
                chat_info = item.get("chatInfo", {})
                contact_info = chat_info["contact"]["localDisplayName"]
                chat_item = item.get("chatItem", {})

                # Only process direct messages
                chat_type = chat_info.get("type")
                if chat_type != "direct":
                    continue

                # Extract the message text
                content = chat_item.get("content", {})
                if isinstance(content, dict) and content.get("type") == "rcvMsgContent":
                    msg_content = content.get("msgContent", {})
                    if (
                        isinstance(msg_content, dict)
                        and msg_content.get("type") == "text"
                    ):
                        text = msg_content.get("text", "")
                    else:
                        continue
                else:
                    continue

                # Get contact information
                contact = chat_info.get("contact", {})
                contact_id = contact.get("contactId")

                if contact_id and text:
                    to_sq: int = int(msg_content["text"])
                    await client.account.send_message(
                        contact_info,
                        f"{to_sq} * {to_sq} is: {to_sq**2}",
                    )


async def main() -> None:
    """Main function to run the bot."""
    bot1, bot2 = await get_bot_clients()
    await bot1.account.create_user(BOT_DISPLAY_NAME, BOT_FULL_NAME)
    await bot1.account.initialize()
    await bot2.account.connect_with_link(
        await bot1.account.get_onetime_connection_link()
    )
    await asyncio.sleep(2)

    # Start processing events
    await process_events(bot1)


if __name__ == "__main__":
    asyncio.run(main())
