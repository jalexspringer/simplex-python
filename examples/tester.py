"""
Test script for simplex_python SDK.
"""

import asyncio
import logging
from simplex_python.client import SimplexClient
from pprint import pprint

from simplex_python.clients.account import ChatType


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


async def connect_the_bots(bot1, bot2):
    # Generate connection link from Bot 1
    print("Generating connection link from Bot 1...")
    conn_link_resp = await bot1.account.get_onetime_connection_link()

    print(f"Bot 1 connection link: {conn_link_resp}")

    # Bot 2 connects to Bot 1 using the link
    print("Bot 2 connecting to Bot 1...")
    connect_resp = await bot2.account.connect_with_link(conn_link_resp)


async def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    bot1, bot2 = await get_bot_clients()

    await connect_the_bots(bot1, bot2)

    # # Wait for the connection to propogate
    # # 2 seconds seems to be enough on a local SMP server
    await asyncio.sleep(2)

    # Get contact list for Bot 1
    connections = await bot2.account.list_connections()
    await bot1.account.create_group("runTheStreets", "No Really We Run")

    # Print a more compact view of the connections
    direct_connections = connections["direct"]
    groups = connections["groups"]
    ds_name = ""

    print(f"\nFound {len(groups)} groups:")
    for group in groups:
        ds_name = group["display_name"]
        pprint(group)
        print(f"Group: {group['display_name']} (ID: {group['group_id']})")
        print(f"Membership Status: {group['membership_status']}")
        print(
            f"  Unread: {group['unread_count']} messages, {group['unread_mentions']} mentions"
        )
        await bot1.account.send_message(
            group["display_name"],
            f"Hello from {bot1.account.active_user_display}",
            ChatType.GROUP,
        )
        if group.get("last_message"):
            print(
                f"  Last message: {group['last_message']} ({group['last_message_ts']})"
            )
            print(f"  {group['last_message_status']}")

        if group["membership_status"] == "invited":
            await bot2.account.accept_group_invite(group["display_name"])
        await bot2.account.send_message(ds_name, "And now bot2 is here", ChatType.GROUP)

        print(f"\nFound {len(direct_connections)} direct connections:")

    for conn in direct_connections:
        print(f"Contact: {conn['display_name']} (ID: {conn['contact_id']})")
        print(f"  Unread: {conn['unread_count']} messages")
        if conn.get("last_message"):
            print(f"  Last message: {conn['last_message']} ({conn['last_message_ts']})")
            print(f"  {conn['last_message_status']}")
            await bot1.account.send_message(
                conn["display_name"], f"Hello from {bot1.account.active_user_display}"
            )
            await bot1.account.add_user_to_group(ds_name, conn["display_name"])

    # Clean up
    await bot1.disconnect()
    await bot2.disconnect()
    print("Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
