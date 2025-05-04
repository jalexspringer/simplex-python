#!/usr/bin/env python3
"""
Simplest possible example of using SimplexClient to connect and get the active user.
Demonstrates the improved response handling with ResponseFactory.
"""

import asyncio
import logging
from typing import Optional
from simplex_python.client import SimplexClient
from simplex_python.responses import ActiveUserResponse

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Server URL - replace with your actual server URL
SERVER_URL = "ws://localhost:5225"  # Default local development server


async def main():
    """Connect to the SimplexClient and get the active user."""
    print("Connecting to Simplex server...")

    # Use the context manager to handle connection and cleanup
    async with SimplexClient(SERVER_URL) as client:
        print("Connected to Simplex server")

        # Get the active user

        # The get_active method now returns a properly typed ActiveUserResponse
        # The ResponseFactory handles the type conversion automatically
        active_user: Optional[ActiveUserResponse] = await client.users.get_active()

        if active_user:
            # The ActiveUserResponse class now exposes properties directly
            print("\n=== User Information ===")
            print(f"User ID: {active_user.user_id}")
            print(f"Display Name: {active_user.display_name}")
            print(f"Full Name: {active_user.full_name}")
            print(f"Local Display Name: {active_user.local_display_name}")

            # Accessing nested data
            print("\n=== Profile Data ===")
            for key, value in active_user.profile.items():
                print(f"{key}: {value}")

            print("\n=== Preferences ===")
            for pref_category, settings in active_user.preferences.items():
                print(f"{pref_category}: {settings}")
        else:
            print("No active user found")


if __name__ == "__main__":
    asyncio.run(main())
