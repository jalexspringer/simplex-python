"""
Squaring Bot Example

A simple bot that responds to numbers by calculating their square.
This is an enhanced version that uses all domain-specific clients of the SimplexPython SDK,
demonstrating the Fluent API pattern with proper error handling and type hints.
"""

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
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FILES_DIR = os.path.join(DATA_DIR, "files")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")


async def setup_directories() -> None:
    """Create necessary directories if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FILES_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logger.info(f"Directories set up: {DATA_DIR}")


async def setup_bot(client: SimplexClient) -> Optional[Dict[str, Any]]:
    """Set up the bot profile and address.

    Args:
        client: The SimplexClient instance

    Returns:
        The user profile if setup is successful, None otherwise
    """
    # Check if we have an active user
    user_response = await client.users.get_active()
    user = None

    if isinstance(user_response, CommandResponse):
        user = user_response.user if hasattr(user_response, "user") else None

    if not user:
        logger.info("No active user profile, creating one...")
        create_response = await client.users.create(BOT_DISPLAY_NAME, BOT_FULL_NAME)
        if isinstance(create_response, CommandResponse):
            user = create_response.user if hasattr(create_response, "user") else None
        else:
            logger.warning("Unexpected response from users.create")
            return None

    # Extract user profile information
    if user and "profile" in user:
        display_name = user["profile"]["displayName"]
        full_name = user["profile"].get("fullName", "")
        logger.info(f"Bot profile: {display_name} ({full_name})")
    else:
        logger.warning("User profile not found in response")
        return None

    # Get or create the user address using fluent API
    address = None
    address_response = await client.users.get_address()
    if isinstance(address_response, CommandResponse):
        # Extract the address from the response
        if hasattr(address_response, "contactLink") and address_response.contactLink:
            address = address_response.contactLink.get("connReqContact")
            logger.info("Using existing contact address")
    else:
        logger.warning("Unexpected response from users.get_address")
        # Create new address if none exists
        create_addr_response = await client.users.create_address()
        address_response = await client.users.get_address()
        if isinstance(address_response, CommandResponse):
            if (
                hasattr(address_response, "contactLink")
                and address_response.contactLink
            ):
                address = address_response.contactLink.get("connReqContact")

    if not address:
        logger.error("Could not get or create bot address.")
        return None

    logger.info(f"Bot address: {address}")

    # Enable automatic acceptance of contact connections
    await client.users.enable_auto_accept(
        accept_incognito=True, auto_reply_text=WELCOME_MSG
    )
    logger.info("Auto-accept enabled for contacts with welcome message")

    return user


async def setup_files(client: SimplexClient) -> bool:
    """Set up file directories for the bot.

    Args:
        client: The SimplexClient instance

    Returns:
        True if setup is successful, False otherwise
    """
    # Set up temporary and files folders
    await client.files.set_temp_folder(os.path.join(DATA_DIR, "temp"))
    await client.files.set_files_folder(FILES_DIR)
    logger.info(f"Files directories configured: {FILES_DIR}")
    return True


async def backup_data(client: SimplexClient) -> bool:
    """Create a backup of the current database.

    Args:
        client: The SimplexClient instance

    Returns:
        True if backup is successful, False otherwise
    """
    # Create a timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"squaring_bot_backup_{timestamp}.simplex")

    # Export the database archive
    await client.database.export_archive(backup_file)
    logger.info(f"Database backup created: {backup_file}")
    return True


async def handle_message(client: SimplexClient, contact_id: int, text: str) -> None:
    """Handle an incoming message from a contact.

    Args:
        client: The SimplexClient instance
        contact_id: The ID of the contact who sent the message
        text: The text content of the message
    """
    # Try to parse the number and calculate square
    try:
        n = float(text)
        reply = f"{n} * {n} = {n * n}"
    except ValueError:
        reply = "This is not a number"

    # Send the response using chats client
    await client.chats.send_message(contact_id, reply)
    logger.info(f"Sent response to contact {contact_id}: {reply}")


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

            # Get additional contact info using the connections client
            if contact_id:
                contact_info = await client.connections.get_contact_info(contact_id)
                logger.info(f"Retrieved detailed info for contact: {contact_name}")

        # Handle new chat items
        elif event_type == "newChatItems":
            chat_items = event.get("chatItems", [])

            for item in chat_items:
                # Extract chat info and item content
                chat_info = item.get("chatInfo", {})
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
                    # Mark the chat as read
                    await client.chats.mark_as_read("direct", contact_id)

                    # Process the message
                    await handle_message(client, contact_id, text)

        # Handle file-related events
        elif event_type in ["fileReceived", "fileReceiving"]:
            file_id = event.get("fileId")
            if file_id:
                logger.info(f"File event received: {event_type}, ID: {file_id}")

                # For demonstration purposes, get the file status
                status = await client.files.get_status(file_id)
                logger.info(f"File status retrieved for ID {file_id}")


async def main() -> None:
    """Main function to run the bot."""
    # Ensure directories exist
    await setup_directories()

    # Define the server as a ChatServer object for type-safety
    server = SERVER_URL if isinstance(SERVER_URL, str) else ChatServer(host=SERVER_URL)

    # Connect to the chat server with async context manager
    async with SimplexClient(server) as client:
        # Set up the bot
        user = await setup_bot(client)
        if not user:
            logger.error("Failed to set up bot user, exiting.")
            return

        # Set up file handling
        if not await setup_files(client):
            logger.warning("Failed to set up file handling, continuing anyway.")

        # Create a backup of the current state
        await backup_data(client)

        # Start processing events
        await process_events(client)


if __name__ == "__main__":
    asyncio.run(main())
