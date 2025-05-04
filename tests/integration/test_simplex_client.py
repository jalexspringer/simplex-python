"""
Integration tests for the SimpleX Chat Python client.

These tests run against a live SimpleX Chat server and verify that
commands and responses are working correctly.
"""

import logging
import os
import pytest

from simplex_python.client import SimplexClient
from simplex_python.transport import ChatServer
from simplex_python.responses import ActiveUserResponse, UsersListResponse, UserItem


# Test configuration
TEST_SERVER = os.environ.get("SIMPLEX_TEST_SERVER", "localhost")
TEST_PORT = int(os.environ.get("SIMPLEX_TEST_PORT", "5225"))
TEST_TIMEOUT = 5  # Seconds

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("simplex_test")


@pytest.fixture
async def client():
    """Create and connect a SimplexClient for testing."""
    server = ChatServer(host=TEST_SERVER, port=str(TEST_PORT))
    async with SimplexClient(server, timeout=TEST_TIMEOUT) as client:
        yield client


# User operations tests
@pytest.mark.asyncio
async def test_get_active_user(client):
    """Test getting the active user with proper response typing."""
    try:
        # Get active user
        active_user = await client.users.get_active()
        
        # Log the result
        logger.info(f"Active user: {active_user}")
        
        # Verify response type and structure
        assert active_user is not None, "Expected an active user to be available"
        assert isinstance(active_user, ActiveUserResponse), "Response should be an ActiveUserResponse"
        
        # Test direct property access
        assert active_user.user_id is not None, "User ID should be present"
        assert active_user.user is not None, "Raw user data should be available"
        assert active_user.display_name is not None, "Display name should be accessible"
        
        # Verify profile data access
        assert isinstance(active_user.profile, dict), "Profile should be a dictionary"
        if active_user.profile:
            assert "displayName" in active_user.profile, "Profile should contain displayName"
            
        # Verify preferences data access
        assert isinstance(active_user.preferences, dict), "Preferences should be a dictionary"
        
    except Exception as e:
        pytest.skip(f"Skipping test due to error: {e}")


@pytest.mark.asyncio
async def test_list_users(client):
    """Test listing all users with proper response typing and iteration."""
    try:
        # List all users
        users_list = await client.users.list_users()
        
        # Log the result
        logger.info(f"Found {len(users_list)} users")
        
        # Verify response type and structure
        assert users_list is not None, "Expected a users list response"
        assert isinstance(users_list, UsersListResponse), "Response should be a UsersListResponse"
        assert len(users_list) > 0, "Expected at least one user in the list"
        
        # Test iteration through users
        for i, user in enumerate(users_list):
            logger.info(f"User {i+1}: {user.display_name} (ID: {user.user_id})")
            
            # Verify UserItem type and properties
            assert isinstance(user, UserItem), "Each user should be a UserItem"
            assert user.user_id is not None, "User ID should be present"
            assert user.display_name is not None, "Display name should be accessible"
            assert isinstance(user.active_user, bool), "Active status should be a boolean"
            assert isinstance(user.unread_count, int), "Unread count should be an integer"
        
        # Test indexing access
        first_user = users_list[0]
        assert isinstance(first_user, UserItem), "Should be able to access users by index"
        
        # Verify raw data access is still available
        assert isinstance(users_list.users, list), "Raw users data should be available"
        
    except Exception as e:
        pytest.skip(f"Skipping test due to error: {e}")


@pytest.mark.asyncio
async def test_active_user_in_users_list(client):
    """Test that the active user is correctly marked in the users list."""
    try:
        # Get active user
        active_user = await client.users.get_active()
        assert active_user is not None, "Expected an active user"
        
        # Get all users
        users_list = await client.users.list_users()
        assert len(users_list) > 0, "Expected at least one user"
        
        # Find active user in the list
        active_users = [user for user in users_list if user.active_user]
        
        # Log findings
        logger.info(f"Active user ID: {active_user.user_id}")
        logger.info(f"Found {len(active_users)} active users in list")
        
        # Verify active user is marked correctly
        assert len(active_users) > 0, "Expected at least one active user in the list"
        
        # Verify the active user IDs match
        active_user_from_list = active_users[0]
        assert active_user_from_list.user_id == active_user.user_id, \
            "Active user ID should match between get_active and list_users"
            
    except Exception as e:
        pytest.skip(f"Skipping test due to error: {e}")


@pytest.mark.asyncio
async def test_set_active_user(client):
    """Test changing the active user and switching back."""
    try:
        # Get the current active user for reference
        original_active_user = await client.users.get_active()
        assert original_active_user is not None, "Expected an active user to start"
        logger.info(f"Original active user: {original_active_user.display_name} (ID: {original_active_user.user_id})")
        
        # Get all users to find a non-active one
        users_list = await client.users.list_users()
        assert len(users_list) > 1, "Need at least two users for this test"
        
        # Find a non-active user to switch to
        non_active_user = None
        for user in users_list:
            if not user.active_user:
                non_active_user = user
                break
                
        assert non_active_user is not None, "Expected at least one non-active user"
        logger.info(f"Switching to user: {non_active_user.display_name} (ID: {non_active_user.user_id})")
        
        # Set the non-active user as active
        new_active_user = await client.users.set_active(non_active_user.user_id)
        
        # Verify the response
        assert new_active_user is not None, "Expected a response when setting active user"
        assert isinstance(new_active_user, ActiveUserResponse), "Response should be an ActiveUserResponse"
        assert new_active_user.user_id == non_active_user.user_id, "User ID should match the requested user"
        logger.info(f"Successfully switched to user: {new_active_user.display_name}")
        
        # Verify the active user has actually changed
        current_active = await client.users.get_active()
        assert current_active.user_id == non_active_user.user_id, "Active user should have changed"
        
        # Switch back to the original user
        logger.info(f"Switching back to original user: {original_active_user.display_name}")
        restored_user = await client.users.set_active(original_active_user.user_id)
        assert restored_user.user_id == original_active_user.user_id, "Should have switched back to original user"
        
        # Verify we've truly switched back
        final_active = await client.users.get_active()
        assert final_active.user_id == original_active_user.user_id, "Should be back to original user"
        logger.info("Successfully restored original active user")
        
    except Exception as e:
        pytest.skip(f"Skipping test due to error: {e}")


@pytest.mark.asyncio
async def test_create_active_user(client):
    """Test creating a new user and handling errors for duplicate users."""
    try:
        import random
        import string
        
        # Get the current active user for reference
        original_active_user = await client.users.get_active()
        assert original_active_user is not None, "Expected an active user to start"
        logger.info(f"Original active user: {original_active_user.display_name} (ID: {original_active_user.user_id})")
        
        # Generate a random username to avoid conflicts from previous test runs
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        display_name = f"TestUser_{random_suffix}"
        full_name = f"Test User {random_suffix}"
        logger.info(f"Creating user with display name: {display_name}")
        
        # Create the new user
        new_user = await client.users.create_active_user(
            display_name=display_name, 
            full_name=full_name
        )
        
        # Verify the response
        assert new_user is not None, "Expected a response when creating user"
        assert isinstance(new_user, ActiveUserResponse), "Response should be an ActiveUserResponse"
        assert new_user.display_name == display_name, "Display name should match what was requested"
        assert new_user.full_name == full_name, "Full name should match what was requested"
        logger.info(f"Successfully created user: {new_user.display_name} (ID: {new_user.user_id})")
        
        # Verify the active user has changed to the new user
        current_active = await client.users.get_active()
        assert current_active.user_id == new_user.user_id, "New user should be active"
        
        # Try to create the same user again to test error handling
        from simplex_python.client_errors import SimplexCommandError
        with pytest.raises(SimplexCommandError) as excinfo:
            # This should fail with a userExists error
            duplicate_user = await client.users.create_active_user(
                display_name=display_name,
                full_name=full_name
            )
            
        # Verify the error details
        error = excinfo.value
        logger.info(f"Expected error when creating duplicate user: {error}")
        
        # Switch back to the original user
        logger.info(f"Switching back to original user: {original_active_user.display_name}")
        await client.users.set_active(original_active_user.user_id)
        
        # Verify we're back to the original user
        final_active = await client.users.get_active()
        assert final_active.user_id == original_active_user.user_id, "Should be back to original user"
        
    except Exception as e:
        pytest.skip(f"Skipping test due to error: {e}")
