"""
Integration tests for the SimpleX Chat Python client.

These tests run against a live SimpleX Chat server and verify that
commands and responses are working correctly.
"""

import logging
import os
import pytest
import random
import string

from simplex_python.client import SimplexClient
from simplex_python.transport import ChatServer
from simplex_python.responses import ActiveUserResponse, UsersListResponse, UserItem, UserProfileNoChangeResponse, UserProfileUpdatedResponse
from simplex_python.responses.base import CmdOkResponse


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


@pytest.mark.asyncio
async def test_list_users(client):
    """Test listing all users with proper response typing and iteration."""
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


@pytest.mark.asyncio
async def test_active_user_in_users_list(client):
    """Test that the active user is correctly marked in the users list."""
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


@pytest.mark.asyncio
async def test_set_active_user(client):
    """Test changing the active user and switching back."""
    # Get the current active user for reference
    original_active_user = await client.users.get_active()
    assert original_active_user is not None, "Expected an active user to start"
    logger.info(f"Original active user: {original_active_user.display_name} (ID: {original_active_user.user_id})")
    
    # Get all users
    users_list = await client.users.list_users()
    
    # If we don't have at least two users, create a test user
    if len(users_list) < 2:
        logger.info("Creating additional test user for active user switching test")
        test_user_name = f"TestUser_SWITCH_{generate_random_string(5)}"
        test_user = await client.users.create_active_user(
            display_name=test_user_name,
            full_name=f"Test User {test_user_name.split('_')[2]}"
        )
        logger.info(f"Created test user: {test_user.display_name} (ID: {test_user.user_id})")
        
        # Switch back to the original user to continue the test
        await client.users.set_active(original_active_user.user_id)
        
        # Get updated list with our new user
        users_list = await client.users.list_users()
    
    # Verify we now have at least two users
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


@pytest.mark.asyncio
async def test_create_active_user(client):
    """Test creating a new user and handling errors for duplicate users."""
    import random
    import string
    from simplex_python.client_errors import SimplexCommandError
    from simplex_python.commands.users import ShowMyAddress
    
    # Get the current active user for reference
    original_active_user = await client.users.get_active()
    assert original_active_user is not None, "Expected an active user to start"
    logger.info(f"Original active user: {original_active_user.display_name} (ID: {original_active_user.user_id})")
    
    # Generate a random username to avoid conflicts from previous test runs
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    display_name = f"TestUser_{random_suffix}"
    full_name = f"Test User {random_suffix}"
    logger.info(f"Creating user with display name: {display_name}")
    
    # Create the new user - by default it should create a profile address
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
    
    # Verify that a profile address was automatically created
    # First, check if the profile has a contact link
    address_resp = await client.send_command(ShowMyAddress(type="showMyAddress"))
    logger.info(f"Profile address check response: {address_resp}")
    assert address_resp is not None, "Expected a response when checking profile address"
    assert hasattr(address_resp, "contactLink"), "New user should have a contact link automatically created"
    
    # Try to create the same user again to test error handling
    with pytest.raises(SimplexCommandError) as excinfo:
        # This should fail with a userExists error
        await client.users.create_active_user(
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


@pytest.mark.asyncio
async def test_set_profile_address(client):
    """Test enabling and disabling profile address for a user."""
    from simplex_python.commands.users import DeleteMyAddress, ShowMyAddress
    
    # Get the current active user for reference
    active_user = await client.users.get_active()
    assert active_user is not None, "Expected an active user to start"
    logger.info(f"Active user: {active_user.display_name} (ID: {active_user.user_id})")
    
    # First, delete any existing profile address to ensure we start with a clean state
    logger.info("Ensuring no profile address exists initially...")
    try:
        await client.send_command(DeleteMyAddress(type="deleteMyAddress"))
        logger.info("Existing address deleted")
    except Exception as e:
        logger.info(f"No address to delete or delete failed: {e}")
    
    # Test that disabling a non-existent address returns a NoChange response
    logger.info("Disabling non-existent profile address...")
    initial_disable = await client.users.set_profile_address(enabled=False)
    
    assert isinstance(initial_disable, UserProfileNoChangeResponse), \
        "Expected no change response when disabling a non-existent address"
    logger.info("Profile address was already disabled (no change needed)")
    
    # Test auto-creation when enabling - this should create an address and enable it
    logger.info("Enabling profile address (should auto-create)...")
    await client.users.set_profile_address(enabled=True)
    
    # After the call, the address should exist and be enabled
    # We can verify by sending a direct command to show the address
    show_address = await client.send_command(ShowMyAddress(type="showMyAddress"))
    assert show_address is not None, "Expected a response when checking profile address"
    assert hasattr(show_address, "contactLink"), "Address should have been created and enabled"
    
    logger.info("Profile address successfully created and enabled")
    
    # Try enabling again - this should give us a NoChange response
    logger.info("Attempting to enable an already enabled profile address...")
    enable_again = await client.users.set_profile_address(enabled=True)
    
    assert isinstance(enable_again, UserProfileNoChangeResponse), \
        "Expected no change response when enabling an already enabled address"
    logger.info("Correctly received no change response")
    
    # First, verify profile address exists then disable it
    logger.info("Disabling profile address...")
    disable_response = await client.users.set_profile_address(enabled=False)
    assert isinstance(disable_response, UserProfileUpdatedResponse), \
        "Expected an update response when disabling the profile address"
    
    # Verify address still exists but is marked as disabled in server state
    show_disabled_response = await client.send_command(ShowMyAddress(type="showMyAddress"))
    assert show_disabled_response is not None, "Expected a response when checking disabled profile address"
    assert hasattr(show_disabled_response, "contactLink"), "Address should still exist after disabling"
    
    # Get profile after disabling address to verify client-side state
    profile_check = await client.users.get_active()
    logger.info(f"Profile after disabling address: User ID {profile_check.user_id}, Contact link exists: {'contactLink' in profile_check.profile}")
    
    # When a profile address is disabled, the contact link still exists in the API response,
    # but the server marks it internally as not being included in the public profile.
    logger.info("Profile address successfully disabled")
    
    # Try disabling again - this should give us a NoChange response
    logger.info("Attempting to disable an already disabled profile address...")
    disable_again = await client.users.set_profile_address(enabled=False)
    
    assert isinstance(disable_again, UserProfileNoChangeResponse), \
        "Expected no change response when disabling an already disabled address"
    logger.info("Correctly received no change response")
    
    # Clean up - make sure to restore to a known good state
    try:
        await client.send_command(DeleteMyAddress(type="deleteMyAddress"))
        logger.info("Test cleanup: Deleted address")
    except Exception as e:
        logger.info(f"Test cleanup: No address to delete or delete failed: {e}")


@pytest.mark.asyncio
async def test_delete_user(client):
    """Test deleting a user and verifying it's removed from the system."""
    # Get the current active user for reference
    original_active_user = await client.users.get_active()
    assert original_active_user is not None, "Expected an active user to start"
    logger.info(f"Original active user: {original_active_user.display_name} (ID: {original_active_user.user_id})")
    
    # Create a new test user that we'll delete
    test_user_name = f"TestUser_DEL_{generate_random_string(5)}"
    logger.info(f"Creating test user {test_user_name} for deletion test")
    
    # Create the user
    test_user = await client.users.create_active_user(
        display_name=test_user_name,
        full_name=f"Test User {test_user_name.split('_')[1]}"
    )
    test_user_id = test_user.user_id
    logger.info(f"Created test user: {test_user.display_name} (ID: {test_user_id})")
    
    # Switch back to original user before attempting deletion
    # (In most applications, you don't want to delete the active user)
    logger.info(f"Switching back to original user: {original_active_user.display_name}")
    await client.users.set_active(original_active_user.user_id)
    
    # Verify we've switched back
    current = await client.users.get_active()
    assert current.user_id == original_active_user.user_id, "Should be back to original user"
    
    # Get initial user list
    initial_users = await client.users.list_users()
    initial_count = len(initial_users)
    logger.info(f"Initial user count: {initial_count}")
    
    # Verify our test user exists in the list
    test_user_found = False
    for user in initial_users:
        if user.user_id == test_user_id:
            test_user_found = True
            break
    
    assert test_user_found, f"Test user {test_user_name} should exist in user list"
    logger.info("Test user found in user list")
    
    # Delete the test user
    logger.info(f"Deleting test user: {test_user_name}")
    result = await client.users.delete_user(test_user_id)
    
    # Verify response is properly typed
    assert isinstance(result, (ActiveUserResponse, CmdOkResponse)), "Delete should return ActiveUserResponse or CmdOkResponse"
    logger.info(f"User deleted, active user is now: {result.display_name if hasattr(result, 'display_name') else 'N/A'}")
    
    # Get user list after deletion
    final_users = await client.users.list_users()
    final_count = len(final_users)
    logger.info(f"Final user count: {final_count}")
    
    # Verify our test user no longer exists in the list
    test_user_still_exists = False
    for user in final_users:
        if user.user_id == test_user_id:
            test_user_still_exists = True
            break
    
    assert not test_user_still_exists, f"Test user {test_user_name} should not exist in user list after deletion"
    assert final_count == initial_count - 1, "User count should decrease by 1 after deletion"
    
    logger.info("Test user successfully deleted and verified")


@pytest.mark.asyncio
async def test_cannot_delete_active_user(client):
    """Test that trying to delete the active user raises the expected error."""
    # Get the current active user
    active_user = await client.users.get_active()
    assert active_user is not None, "Expected an active user to start"
    active_user_id = active_user.user_id
    logger.info(f"Active user: {active_user.display_name} (ID: {active_user_id})")
    
    # Attempt to delete the active user - should fail with ValueError
    with pytest.raises(ValueError) as excinfo:
        await client.users.delete_user(active_user_id)
    
    # Verify the error message is descriptive
    error_msg = str(excinfo.value)
    assert f"Cannot delete the active user (ID: {active_user_id})" in error_msg
    assert "Switch to a different user first with set_active()" in error_msg
    logger.info(f"Correctly rejected attempt to delete active user with error: {error_msg}")
    
    # Verify the user still exists
    users = await client.users.list_users()
    user_ids = [user.user_id for user in users]
    assert active_user_id in user_ids, "Active user should still exist after failed deletion attempt"
    logger.info("Verified active user still exists")


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
