"""
Account Client Example

This example demonstrates common operations with the SimplexClient.account client.
It shows how to create users, connect users, send messages, and work with groups.
"""

import asyncio
import logging
from pprint import pprint

from simplex_python.client import SimplexClient
from simplex_python.clients.account import ChatType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
SERVER_URL_1 = "ws://localhost:5225"
SERVER_URL_2 = "ws://localhost:5226"


async def setup_client(
    server_address: str, display_name: str = None, full_name: str = None
) -> SimplexClient:
    """Set up a client with the given server address and optional user details."""
    # Initialize and connect the client
    client = SimplexClient(server_address)
    await client.connect()

    # Create a new user if display_name is provided
    if display_name and full_name:
        await client.account.create_user(display_name, full_name)

    # Initialize the client's account data
    await client.account.initialize()
    # for i in range(3):
    #     await client.account.remove_connection(i + 1)

    # Display connection information
    logger.info(
        f"Connected: {client.account.active_user_display} --- ID: {client.account.active_user_id}"
    )

    return client


async def demonstrate_account_operations():
    """Demonstrate various operations with the account client."""

    # Setup two clients
    client1 = await setup_client(SERVER_URL_1)  # , "User1", "Test User One")
    client2 = await setup_client(SERVER_URL_2)  # , "User2", "Test User Two")

    try:
        # 1. Generate a connection link for User1
        logger.info("Generating connection link from User1...")
        connection_link = await client1.account.get_onetime_connection_link()
        logger.info(f"Connection link generated: {connection_link}")

        # 2. User2 connects to User1 using the link
        logger.info("User2 connects to User1...")
        await client2.account.connect_with_link(connection_link)
        logger.info("Connection established")

        # Wait for connection to propagate
        await asyncio.sleep(2)

        # 3. List connections for both users
        logger.info("Listing connections for User1:")
        user1_connections = await client1.account.list_connections()
        direct_connections = user1_connections["direct"]

        for conn in direct_connections:
            logger.info(f"Contact: {conn['display_name']} (ID: {conn['contact_id']})")

        # 4. Send a direct message
        if direct_connections:
            contact_name = direct_connections[0]["display_name"]
            logger.info(f"Sending message to {contact_name}...")
            await client1.account.send_message(
                contact_name, "Hello! This is a direct message from User1."
            )

        # 5. Create a group
        group_name = "TestGroup"
        logger.info(f"Creating group '{group_name}'...")
        await client1.account.create_group(group_name, "A test group")

        # 6. Add User2 to the group
        if direct_connections:
            contact_name = direct_connections[0]["display_name"]
            logger.info(f"Adding {contact_name} to group...")
            await client1.account.add_user_to_group(group_name, contact_name)

        # 7. User2 accepts group invitation
        await asyncio.sleep(2)
        user2_connections = await client2.account.list_connections()
        groups = user2_connections["groups"]

        for group in groups:
            if group["membership_status"] == "invited":
                logger.info(
                    f"User2 accepting invitation to group {group['display_name']}..."
                )
                await client2.account.accept_group_invite(group["display_name"])

        # 8. Send a group message
        logger.info(f"Sending message to group {group_name}...")
        await client1.account.send_message(
            group_name, "Hello everyone in the group!", ChatType.GROUP
        )

        # Wait for messages to be delivered
        await asyncio.sleep(2)

    finally:
        # Clean up
        await client1.disconnect()
        await client2.disconnect()
        logger.info("Clients disconnected")


async def main():
    await demonstrate_account_operations()
    logger.info("Account operations example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
