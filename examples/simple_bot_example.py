"""
Simple Event-Listening Bot Example

This example demonstrates how to create a bot that listens for events
using the SimplexClient.events() async generator and responds to messages.
"""

import asyncio
import logging
from typing import Optional
from pprint import pprint

from simplex_python.client import SimplexClient
from simplex_python.responses import CommandResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration constants
SERVER_URL = "ws://localhost:5225"
BOT_DISPLAY_NAME = "SimpleBot"
BOT_FULL_NAME = "Simple Event Listener Bot"
WELCOME_MESSAGE = (
    "Hello! I'm a simple echo bot. Send me a message and I'll echo it back."
)


async def setup_bot(server_address: str) -> SimplexClient:
    """Set up a bot with the given server address.

    Args:
        server_address: WebSocket URL of the chat server

    Returns:
        A connected SimplexClient instance
    """
    # Initialize and connect the client
    client = SimplexClient(server_address)
    await client.connect()

    # Initialize the client's account data
    await client.account.initialize()

    logger.info(
        f"Bot connected: {client.account.active_user_display} (ID: {client.account.active_user_id})"
    )

    return client


async def process_events(client: SimplexClient) -> None:
    """Process incoming events from the chat server.

    Listens for new messages and responds to them.

    Args:
        client: The SimplexClient instance
    """
    logger.info("Starting to process events...")

    # Process incoming events using the events() async generator
    async for event in client.events():
        # Skip non-dict events
        if not isinstance(event, dict):
            continue

        event_type = event.get("type")

        # Handle contact connection events
        if event_type == "contactConnected":
            contact = event.get("contact", {})
            contact_profile = contact.get("profile", {})
            contact_name = contact_profile.get("displayName", "Unknown")
            logger.info(f"Contact connected: {contact_name}")

            # Send welcome message to new contact
            await client.account.send_message(contact_name, WELCOME_MESSAGE)

        # Handle new chat items (messages)
        elif event_type == "newChatItems":
            chat_items = event.get("chatItems", [])

            for item in chat_items:
                # Extract message info
                chat_info = item.get("chatInfo", {})
                chat_type = chat_info.get("type")

                # Only process direct messages
                if chat_type != "direct":
                    continue

                # Get contact information
                contact = chat_info.get("contact", {})
                contact_name = contact.get("localDisplayName", "Unknown")

                # Extract message content
                chat_item = item.get("chatItem", {})
                content = chat_item.get("content", {})

                # Process only received text messages
                if isinstance(content, dict) and content.get("type") == "rcvMsgContent":
                    msg_content = content.get("msgContent", {})
                    if (
                        isinstance(msg_content, dict)
                        and msg_content.get("type") == "text"
                    ):
                        # Extract the message text
                        text = msg_content.get("text", "")

                        if text:
                            logger.info(f"Received message from {contact_name}: {text}")

                            # Echo the message back
                            response = f"You said: {text}"
                            logger.info(
                                f"Sending response to {contact_name}: {response}"
                            )

                            await client.account.send_message(contact_name, response)


async def main() -> None:
    """Main function to set up and run the bot."""
    try:
        # Set up the bot
        logger.info("Setting up bot...")
        bot = await setup_bot(SERVER_URL)

        # Create a new user for the bot if needed
        # Uncomment the following line to create a new user
        # await bot.account.create_user(BOT_DISPLAY_NAME, BOT_FULL_NAME)

        # Start processing events
        print(bot.account.active_user_contact_link)
        await process_events(bot)

    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        # This will likely never be reached as process_events runs indefinitely
        logger.info("Disconnecting bot...")
        await bot.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
