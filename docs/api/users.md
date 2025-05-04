# Users API

The Users API provides comprehensive functionality for managing user profiles, identities, and connections in the SimpleX Chat system.

## UsersClient

The `UsersClient` class is accessible as a property of the main `SimplexClient` object via `client.users`.

::: simplex_python.clients.users.UsersClient
    options:
      show_source: true
      show_signature_annotations: true
      show_root_heading: true

## User Commands

User management commands are defined in the commands.users module.

::: simplex_python.commands.users
    options:
      show_source: true
      members: [APICreateActiveUser, APIShowActiveUser, APISetActiveUser, APIShowUsers, APIDeleteUser]
      
## Response Types

User-specific response types provide strongly typed access to server responses.

::: simplex_python.responses.users
    options:
      show_source: true
      show_signature_annotations: true

## Examples

### Creating a User

```python
# Create a new user and set as active
new_user = await client.users.create_active_user(
    display_name="Alice",
    full_name="Alice Smith"
)

# Access typed properties directly
print(f"Created user {new_user.display_name} with ID {new_user.user_id}")
```

### Managing Users

```python
# List all users
users = await client.users.list_users()
print(f"Found {len(users)} users")

for user in users:
    print(f"User {user.user_id}: {user.display_name}")
    
# Switch to another user
await client.users.set_active(user_id=2)

# Delete a user when no longer needed
await client.users.delete_user(user_id=3)
```

### Error Handling

```python
try:
    # Will raise ValueError if attempting to delete active user
    await client.users.delete_user(user_id=active_user_id)
except ValueError as e:
    print(f"Cannot delete active user: {e}")
    
# Switch to another user first
await client.users.set_active(another_user_id)
# Now delete is allowed
await client.users.delete_user(active_user_id)