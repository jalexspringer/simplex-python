import asyncio
from simplexbot.client import SimplexClient
from simplexbot.command import ShowActiveUser, ListUsers

async def main():
    # Connect to the running simplex-chat server
    async with SimplexClient("ws://localhost:5225") as client:
        print("Connected!")

        # Example 1: Show active user (use dataclass command)
        resp = await client.send_command(ShowActiveUser())
        print("ShowActiveUser response:", resp)

        # Example 2: List users (use dataclass command)
        resp2 = await client.send_command(ListUsers())
        print("ListUsers response:", resp2)

        # Optionally, listen for server events
        print("Listening for events (Ctrl+C to exit):")
        async for event in client.events():
            print("Event:", event)

if __name__ == "__main__":
    asyncio.run(main())
