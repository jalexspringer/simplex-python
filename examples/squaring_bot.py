"""
Squaring Bot Example

A simple bot that responds to numbers by calculating their square.
This is the Python equivalent of the TypeScript squaring-bot.js example,
updated to use the Fluent API pattern.
"""

import asyncio
import logging
from simplex_python.client import SimplexClient
from simplex_python.errors import SimplexCommandError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

SERVER_URL = "ws://localhost:5225"
WELCOME_MSG = "Hello! I am a simple squaring bot - if you send me a number, I will calculate its square"


async def main():
    # Connect to the chat server
    async with SimplexClient(SERVER_URL) as client:
        try:
            # Check if we have an active user
            user = await client.users.get_active()
            if not user:
                logger.info("No active user profile, creating one...")
                await client.users.create("SquaringBot", "Python Squaring Bot")
                user = await client.users.get_active()
            
            # Extract user profile information
            display_name = user["profile"]["displayName"]
            full_name = user["profile"].get("fullName", "")
            logger.info(f"Bot profile: {display_name} ({full_name})")

            # Get or create the user address using fluent API
            try:
                address = await client.users.get_address()
                logger.info("Using existing contact address")
            except SimplexCommandError:
                logger.info("Creating new contact address")
                await client.users.create_address()
                address = await client.users.get_address()
                
            if not address:
                logger.error("Could not get or create bot address.")
                return
                
            logger.info(f"Bot address: {address}")

            # Enable automatic acceptance of contact connections
            await client.users.enable_auto_accept(accept_incognito=True)
            logger.info("Auto-accept enabled for contacts")

            # Process incoming messages
            async for event in client.events():
                event_type = event.get("type")

                # Handle contact connected event
                if event_type == "contactConnected":
                    contact = event["contact"]
                    contact_id = contact["contactId"]
                    contact_name = contact["profile"]["displayName"]
                    logger.info(f"{contact_name} connected")

                    # Send welcome message using chats client
                    await client.chats.send_message(contact_id, WELCOME_MSG)

                # Handle new chat items
                elif event_type == "newChatItems":
                    chat_items = event["chatItems"]

                    for item in chat_items:
                        # Extract chat info and item content
                        chat_info = item["chatInfo"]
                        chat_item = item["chatItem"]

                        # Only process direct messages
                        chat_type = chat_info["type"]
                        if chat_type != "direct":
                            continue

                        # Extract the message text
                        content = chat_item["content"]
                        if (
                            isinstance(content, dict)
                            and content.get("type") == "rcvMsgContent"
                        ):
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

                        # Try to parse the number and calculate square
                        try:
                            n = float(text)
                            reply = f"{n} * {n} = {n * n}"
                        except ValueError:
                            reply = "This is not a number"

                        # Send the response using chats client
                        contact = chat_info["contact"]
                        contact_id = contact["contactId"]
                        await client.chats.send_message(contact_id, reply)
                        
        except SimplexCommandError as e:
            logger.error(f"Command error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
