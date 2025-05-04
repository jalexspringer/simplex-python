#!/usr/bin/env python3
"""
Example usage of SimplexClient showing user operations.

Demonstrates:
1. Connecting to a Simplex server
2. Getting the active user with fluent API
3. Listing all users and accessing user properties
4. Changing the active user
5. Creating a new user account
"""

import asyncio
import logging
import random
import string
from typing import Optional
from simplex_python.client import SimplexClient
from simplex_python.responses import ActiveUserResponse, UsersListResponse
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

        # --- Get Active User ---
        active_user: Optional[ActiveUserResponse] = await client.users.get_active()
        if active_user:
            print("\n=== Active User Information ===")
            print(f"User ID: {active_user.user_id}")
            print(f"Display Name: {active_user.display_name}")
            print(f"Full Name: {active_user.full_name}")
        else:
            print("No active user found")

        # --- List All Users ---
        try:
            users: UsersListResponse = await client.users.list_users()

            print(f"\n=== Found {len(users)} Users ===")

            # Iterate through all users
            for i, user in enumerate(users):
                print(f"\nUser {i + 1}:")
                print(f"  ID: {user.user_id}")
                print(f"  Display Name: {user.display_name}")
                print(f"  Full Name: {user.full_name}")
                print(f"  Active: {'Yes' if user.active_user else 'No'}")
                print(f"  Unread Messages: {user.unread_count}")

                # Show preferences example
                if user.preferences:
                    print("  Preferences:")
                    for pref_name, pref_value in user.preferences.items():
                        print(f"    {pref_name}: {pref_value}")

        except Exception as e:
            print(f"Error listing users: {e}")

        # --- Demonstrate Changing Active User ---
        try:
            # Find a non-active user to switch to
            non_active_user = None
            for user in users:
                if not user.active_user:
                    non_active_user = user
                    break

            if non_active_user:
                print(
                    f"\n=== Switching to User: {non_active_user.display_name} (ID: {non_active_user.user_id}) ==="
                )

                # Set as active user
                new_active = await client.users.set_active(non_active_user.user_id)

                print(f"Successfully switched to user: {new_active.display_name}")
                print(f"User ID: {new_active.user_id}")
                print(f"Full Name: {new_active.full_name}")

                active_user: Optional[
                    ActiveUserResponse
                ] = await client.users.get_active()
                if active_user:
                    print("\n=== Active User Information ===")
                    print(f"User ID: {active_user.user_id}")
                    print(f"Display Name: {active_user.display_name}")
                    print(f"Full Name: {active_user.full_name}")
                else:
                    print("No active user found")

                # Switch back to original user
                if active_user:
                    print(
                        f"\n=== Switching back to original user: {active_user.display_name} ==="
                    )
                    await client.users.set_active(active_user.user_id)
                    print("Switched back to original user")
            else:
                print("\nNo non-active users found to demonstrate switching")

        except Exception as e:
            print(f"Error changing active user: {e}")

        # --- Demonstrate Creating a New User ---
        try:
            # Generate a random username to avoid conflicts
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            display_name = f"TestUser_{random_suffix}"
            full_name = f"Test User {random_suffix}"

            print(f"\n=== Creating New User: {display_name} ===")

            # Create new user
            new_user = await client.users.create_active_user(
                display_name=display_name,
                full_name=full_name
            )

            print(f"Successfully created user:")
            print(f"  User ID: {new_user.user_id}")
            print(f"  Display Name: {new_user.display_name}")
            print(f"  Full Name: {new_user.full_name}")

            # Try to create the same user again to demonstrate error handling
            print(f"\n=== Attempting to create duplicate user {display_name} ===")
            try:
                duplicate_user = await client.users.create_active_user(
                    display_name=display_name,
                    full_name=full_name
                )
            except SimplexCommandError as e:
                # Parse the error to check if it's a "userExists" error
                if hasattr(e, 'error') and isinstance(e.error, dict):
                    error_type = e.error.get('errorType', {})
                    if isinstance(error_type, dict) and error_type.get('type') == 'userExists':
                        print(f"User already exists: {error_type.get('contactName')}")
                    else:
                        print(f"Error creating user: {e}")
                else:
                    print(f"Error creating user: {e}")

            # Switch back to the original user if we had one
            if active_user and active_user.user_id != new_user.user_id:
                print(f"\n=== Switching back to original user: {active_user.display_name} ===")
                await client.users.set_active(active_user.user_id)
                print("Switched back to original user")

        except Exception as e:
            print(f"Error creating user: {e}")


if __name__ == "__main__":
    asyncio.run(main())
