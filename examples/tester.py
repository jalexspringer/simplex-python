#!/usr/bin/env python3
"""
Example usage of SimplexClient showing user operations.

Demonstrates:
1. Connecting to a Simplex server
2. Getting the active user with fluent API
3. Listing all users and accessing user properties
4. Changing the active user
5. Creating a new user account
6. Configuring user profile address
7. Deleting a user account
"""

import asyncio
import logging
import random
import string
from typing import Optional
from simplex_python.client import SimplexClient
from simplex_python.responses import (
    ActiveUserResponse,
    UserProfileUpdatedResponse,
    UserProfileNoChangeResponse,
)
from simplex_python.responses.base import CmdOkResponse
from simplex_python.client_errors import SimplexCommandError

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Server URL - replace with your actual server URL
SERVER_URL = "ws://localhost:5225"  # Default local development server


async def main():
    """Connect to the SimplexClient and perform user operations."""
    print("Connecting to Simplex server...")

    # Use the context manager to handle connection and cleanup
    async with SimplexClient(SERVER_URL) as client:
        print("Connected to Simplex server")

        # --- Demonstrate Listing Users ---
        print("\n=== Found", await client.users.list_users())
        await client.users.create_active_user("ME!", "REALLY ME")
        # --- Demonstrate User Deletion ---
        # List users before deletion
        users_before = await client.users.list_users()
        print(f"\n=== Found {users_before} users before deletion ===")

        test_user_id = 2
        print(f"\n=== Deleting user (ID: {test_user_id}) ===")
        try:
            # Make sure we're not deleting the active user to avoid complications
            current_active = await client.users.get_active()
            if current_active.user_id == test_user_id:
                # Find another user to switch to
                for user in users_before:
                    if user.user_id != test_user_id:
                        print(f"Switching to user {user.display_name} before deletion")
                        await client.users.set_active(user.user_id)
                        break

            # Delete the test user
            result = await client.users.delete_user(test_user_id)

            # Handle both possible success response types
            if isinstance(result, ActiveUserResponse):
                print(f"User deleted, new active user is: {result.display_name}")
            elif isinstance(result, CmdOkResponse):
                print("User deleted successfully")
            else:
                print(
                    f"User deletion completed with response type: {type(result).__name__}"
                )

            # Verify deletion by listing users again
            users_after = await client.users.list_users()
            print(f"\n=== Found {len(users_after)} users after deletion ===")

            # Check if user still exists (shouldn't, but verify)
            for user in users_after:
                if user.user_id == test_user_id:
                    print(
                        f"Warning: User with ID {test_user_id} still exists after deletion"
                    )
                    break
            else:
                print(f"Success: User with ID {test_user_id} was deleted completely")

        except SimplexCommandError as e:
            if "userUnknown" in str(e):
                print(f"Error: User with ID {test_user_id} doesn't exist")
            else:
                print(f"Error deleting user: {e}")


if __name__ == "__main__":
    asyncio.run(main())
