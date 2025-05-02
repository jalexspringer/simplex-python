"""
SimpleX Chat WebSocket API Documentation Generator

This script connects to a SimpleX Chat WebSocket server, tests commands,
and generates comprehensive API documentation by:
1. Parsing Controller.hs to extract all command types
2. Using JSON schema to understand message formats
3. Testing commands against a running instance
4. Generating markdown documentation with enhanced descriptions and error handling guidance
"""

import asyncio
import json
import logging
import re
import sys
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable
import websockets
import argparse
from dataclasses import dataclass, field
from urllib.request import urlopen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("simplex_api_doc.log"),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class CommandInfo:
    """Information about a SimpleX Chat command"""

    name: str
    description: str = "No description available"
    parameters: Dict[str, Dict[str, str]] = field(default_factory=dict)
    example: str = ""
    responses: List[Dict[str, Any]] = field(default_factory=list)
    response_types: Set[str] = field(default_factory=set)
    category: str = "Uncategorized"
    api_prefix: bool = False  # Indicates if this is an API command (starts with _)
    chat_command_variant: Optional[str] = None  # The actual variant in ChatCommand
    error_patterns: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Common errors and solutions

    def api_name(self) -> str:
        """Return the API name if this is an API command"""
        if self.chat_command_variant and self.chat_command_variant.startswith("API"):
            return self.chat_command_variant
        return None


@dataclass
class ResponseInfo:
    """Information about a SimpleX Chat response type"""

    name: str
    description: str = "No description available"
    schema: Dict[str, Any] = field(default_factory=dict)
    examples: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SchemaInfo:
    """Information about a schema definition"""

    name: str
    schema: Dict[str, Any]
    description: str = "No description available"


@dataclass
class ErrorInfo:
    """Information about a common error pattern"""

    error_type: str
    message: str
    cause: str
    solution: str


class SimpleXAPIDocumenter:
    def __init__(
        self,
        url: str = "ws://localhost:5226",
        controller_path: str = None,
        schema_path: str = None,
    ):
        """Initialize the documenter with connection and source paths"""
        self.url = url
        self.websocket = None
        self.current_corr_id = 0
        self.command_responses: Dict[str, List[Dict[str, Any]]] = {}
        self.commands: Dict[str, CommandInfo] = {}
        self.responses: Dict[str, ResponseInfo] = {}
        self.schema_definitions: Dict[str, SchemaInfo] = {}
        self.active_user_id = None
        self.controller_path = controller_path
        self.schema_path = schema_path
        self.common_errors: Dict[str, ErrorInfo] = {}

        # Resource tracking
        self.resources = {
            "users": [],
            "contacts": [],
            "groups": [],
            "files": [],
            "messages": [],
        }

        # Commands mapping to categories
        self.command_categories = {
            "User Management": [
                "/u",
                "/users",
                "/_create",
                "/_user",
                "/_profile",
                "ShowActiveUser",
                "CreateActiveUser",
                "ListUsers",
                "APISetActiveUser",
                "SetActiveUser",
                "ShowProfile",
                "UpdateProfile",
                "UpdateProfileImage",
                "APIUpdateProfile",
            ],
            "Chat Management": [
                "/_start",
                "/_stop",
                "/_get chats",
                "/_get chat",
                "StartChat",
                "CheckChatRunning",
                "APIStopChat",
                "APIActivateChat",
                "APISuspendChat",
            ],
            "Messaging": [
                "/_send",
                "/_update item",
                "/_delete item",
                "SendMessage",
                "SendLiveMessage",
                "EditMessage",
                "DeleteMessage",
                "APISendMessages",
            ],
            "Contact Management": [
                "/_connect",
                "/_accept",
                "/_reject",
                "/_set alias",
                "/_show_address",
                "/_create_address",
                "/_delete_address",
                "AcceptContact",
                "RejectContact",
                "APIAddContact",
                "AddContact",
                "APIListContacts",
                "ListContacts",
            ],
            "Group Management": [
                "/_group",
                "/_add",
                "/_join",
                "/_remove",
                "/_leave",
                "/_members",
                "/_group_profile",
                "/_create link",
                "/_delete link",
                "NewGroup",
                "APINewGroup",
                "AddMember",
                "JoinGroup",
                "RemoveMembers",
                "LeaveGroup",
                "DeleteGroup",
                "ListMembers",
                "CreateGroupLink",
                "DeleteGroupLink",
            ],
            "File Transfer": [
                "/freceive",
                "/fcancel",
                "/fstatus",
                "SendFile",
                "SendImage",
                "ReceiveFile",
                "CancelFile",
                "FileStatus",
            ],
            "Call Management": [
                "APISendCallInvitation",
                "SendCallInvitation",
                "APIRejectCall",
                "APISendCallOffer",
                "APISendCallAnswer",
                "APISendCallExtraInfo",
                "APIEndCall",
                "APIGetCallInvitations",
            ],
            "Network & Settings": [
                "APISetNetworkConfig",
                "APIGetNetworkConfig",
                "SetNetworkConfig",
                "ReconnectAllServers",
                "ReconnectServer",
                "APIGetNetworkStatuses",
                "SetLocalDeviceName",
            ],
            "Remote Control": [
                "ListRemoteHosts",
                "StartRemoteHost",
                "SwitchRemoteHost",
                "StopRemoteHost",
                "DeleteRemoteHost",
                "StoreRemoteFile",
                "GetRemoteFile",
                "ConnectRemoteCtrl",
                "ListRemoteCtrls",
            ],
        }

        # Initialize common errors
        self._init_common_errors()

        # Initialize with enhanced command descriptions for common commands
        self._init_command_descriptions()

    def _init_common_errors(self):
        """Initialize common error patterns and solutions"""
        self.common_errors = {
            "chat_not_started": ErrorInfo(
                error_type="commandError",
                message="Chat not started",
                cause="Attempting to run commands before starting the chat system",
                solution="Always call /_start first after checking the active user with /u",
            ),
            "invalid_syntax": ErrorInfo(
                error_type="commandError",
                message="Failed reading: empty",
                cause="Command parameters are missing or improperly formatted",
                solution="Verify parameter format and ensure all required parameters are provided",
            ),
            "contact_not_found": ErrorInfo(
                error_type="errorStore",
                message="contactNotFound",
                cause="Referenced contact does not exist",
                solution="Verify contact ID exists before operations by listing contacts first",
            ),
            "group_not_found": ErrorInfo(
                error_type="errorStore",
                message="groupNotFound",
                cause="Referenced group does not exist",
                solution="Verify group ID exists before operations by listing groups first",
            ),
            "user_not_found": ErrorInfo(
                error_type="errorStore",
                message="userNotFound",
                cause="Referenced user does not exist",
                solution="Check user ID with /users before trying to set active user",
            ),
            "item_not_found": ErrorInfo(
                error_type="errorChat",
                message="messageNotFound",
                cause="Referenced message does not exist or was deleted",
                solution="Verify message exists before editing or deleting it",
            ),
            "network_error": ErrorInfo(
                error_type="errorAgent",
                message="networkError",
                cause="Network connectivity issues or SMP server unreachable",
                solution="Check network connectivity and SMP server status",
            ),
            "permission_error": ErrorInfo(
                error_type="errorChat",
                message="notAllowed",
                cause="Insufficient permissions for the requested operation",
                solution="Verify user has appropriate permissions for this action",
            ),
            "json_parsing_error": ErrorInfo(
                error_type="commandError",
                message="Failed reading: invalid syntax",
                cause="Malformed JSON in command parameters",
                solution="Ensure JSON is properly formatted and escaped",
            ),
        }

    async def connect(self):
        """Connect to the SimpleX WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.url)
            logger.info(f"Connected to SimpleX server at {self.url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SimpleX server: {e}")
            return False

    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from SimpleX server")

    def next_corr_id(self) -> str:
        """Generate a new correlation ID for commands"""
        self.current_corr_id += 1
        return str(self.current_corr_id)

    async def send_command(
        self, cmd: str, expect_response: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Send a command to the server and wait for a response"""
        if not self.websocket:
            logger.error("WebSocket not connected")
            return None

        corr_id = self.next_corr_id()
        message = json.dumps({"corrId": corr_id, "cmd": cmd})

        logger.info(f"Sending: {message}")
        await self.websocket.send(message)

        if expect_response:
            try:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                logger.info(f"Received: {json.dumps(response_data, indent=2)}")

                # Record this command-response pair
                cmd_key = cmd.split()[0] if " " in cmd else cmd
                if cmd_key not in self.command_responses:
                    self.command_responses[cmd_key] = []
                self.command_responses[cmd_key].append(response_data)

                # Update our tracking of resources
                self._update_resources(cmd, response_data)

                # Update response types
                if (
                    cmd_key in self.commands
                    and "resp" in response_data
                    and "type" in response_data["resp"]
                ):
                    self.commands[cmd_key].response_types.add(
                        response_data["resp"]["type"]
                    )

                # Record error patterns
                if (
                    "resp" in response_data
                    and response_data["resp"].get("type") == "chatCmdError"
                ):
                    self._record_error_pattern(cmd_key, response_data)

                return response_data
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for response to: {cmd}")
                return None
            except Exception as e:
                logger.error(f"Error receiving response: {e}")
                return None

        return None

    def _record_error_pattern(self, cmd_key: str, response: Dict[str, Any]):
        """Record error patterns for commands to improve documentation"""
        if cmd_key not in self.commands:
            return

        error_data = response.get("resp", {}).get("chatError", {})
        error_type = error_data.get("type")

        if not error_type:
            return

        error_info = {"type": error_type, "data": error_data, "response": response}

        # Add to command's error patterns
        if error_info not in self.commands[cmd_key].error_patterns:
            self.commands[cmd_key].error_patterns.append(error_info)

    def _update_resources(self, cmd: str, response: Dict[str, Any]):
        """Update tracked resources based on command responses"""
        try:
            resp_data = response.get("resp", {})
            resp_type = resp_data.get("type")

            # Track users
            if resp_type == "activeUser" and "user" in resp_data:
                user_id = resp_data["user"].get("userId")
                if user_id and user_id not in self.resources["users"]:
                    self.resources["users"].append(user_id)
                    self.active_user_id = user_id

            # Track users list
            elif resp_type == "usersList" and "users" in resp_data:
                for user_info in resp_data["users"]:
                    if "user" in user_info and "userId" in user_info["user"]:
                        user_id = user_info["user"]["userId"]
                        if user_id not in self.resources["users"]:
                            self.resources["users"].append(user_id)

            # Track contacts
            elif (
                resp_type in ["contactConnected", "contactInfo"]
                and "contact" in resp_data
            ):
                contact_id = resp_data["contact"].get("contactId")
                if contact_id and contact_id not in self.resources["contacts"]:
                    self.resources["contacts"].append(contact_id)

            # Track groups
            elif (
                resp_type in ["groupCreated", "groupInfo"] and "groupInfo" in resp_data
            ):
                group_id = resp_data["groupInfo"].get("groupId")
                if group_id and group_id not in self.resources["groups"]:
                    self.resources["groups"].append(group_id)

            # Track messages
            elif (
                resp_type in ["chatItems", "newChatItems"] and "chatItems" in resp_data
            ):
                for item in resp_data["chatItems"]:
                    if "chatItem" in item and "meta" in item["chatItem"]:
                        item_id = item["chatItem"]["meta"].get("itemId")
                        if item_id and item_id not in self.resources["messages"]:
                            self.resources["messages"].append(item_id)
        except Exception as e:
            logger.warning(f"Error updating resources: {e}")

    def _init_command_descriptions(self):
        """Initialize enhanced descriptions for common commands"""
        # Add detailed descriptions for common commands
        basic_commands = {
            "/u": CommandInfo(
                name="/u",
                description="Show the currently active user profile with details including user ID, display name, and preferences.",
                category="User Management",
            ),
            "/users": CommandInfo(
                name="/users",
                description="List all user profiles configured on this SimpleX Chat instance, including their IDs, display names, and active status.",
                category="User Management",
            ),
            "/_create": CommandInfo(
                name="/_create",
                description="Create a new user profile with specified display name, full name, and server configuration.",
                parameters={
                    "profile": {
                        "type": "object",
                        "description": "User profile information object containing displayName (required) and fullName (optional)",
                    },
                    "sameServers": {
                        "type": "boolean",
                        "description": "Whether to use the same SMP servers as existing users",
                    },
                    "pastTimestamp": {
                        "type": "boolean",
                        "description": "Whether to set the creation timestamp in the past",
                    },
                },
                example='/_create user {"profile":{"displayName":"Alice","fullName":"Alice Smith"},"sameServers":true,"pastTimestamp":false}',
                category="User Management",
                api_prefix=True,
            ),
            "/_user": CommandInfo(
                name="/_user",
                description="Set a different user as the active user by specifying their user ID.",
                parameters={
                    "userId": {
                        "type": "integer",
                        "description": "The numeric ID of the user to activate",
                    }
                },
                example="/_user 1",
                category="User Management",
                api_prefix=True,
            ),
            "/_start": CommandInfo(
                name="/_start",
                description="Start the chat system, enabling messaging capabilities. This command must be executed before most other commands will work.",
                parameters={
                    "subscribe": {
                        "type": "string",
                        "description": "Whether to subscribe to connection events (on/off)",
                    },
                    "expire": {
                        "type": "string",
                        "description": "Whether to enable message expiration (on/off)",
                    },
                    "xftp": {
                        "type": "string",
                        "description": "Whether to start XFTP workers for file transfers (on/off)",
                    },
                },
                example="/_start subscribe=on expire=on xftp=on",
                category="Chat Management",
                api_prefix=True,
            ),
            "/_stop": CommandInfo(
                name="/_stop",
                description="Stop the chat system, disabling messaging capabilities until /_start is called again.",
                category="Chat Management",
                api_prefix=True,
            ),
            "/_get chats": CommandInfo(
                name="/_get chats",
                description="Get the list of all chats (contacts and groups) for the current user, with optional inclusion of pending connections.",
                parameters={
                    "pcc": {
                        "type": "string",
                        "description": "Include pending connections (on/off)",
                    }
                },
                example="/_get chats pcc=on",
                category="Chat Management",
                api_prefix=True,
            ),
            "/_get chat": CommandInfo(
                name="/_get chat",
                description="Get messages for a specific chat with pagination support.",
                parameters={
                    "chatId": {
                        "type": "string",
                        "description": "The chat ID with prefix '@' for contacts or '#' for groups",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Maximum number of messages to return",
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset from the most recent message (for pagination)",
                    },
                },
                example="/_get chat @1 count=10 offset=0",
                category="Chat Management",
                api_prefix=True,
            ),
            "/_send": CommandInfo(
                name="/_send",
                description="Send a message to a specific chat (contact or group).",
                parameters={
                    "chatId": {
                        "type": "string",
                        "description": "The chat ID with prefix '@' for contacts or '#' for groups",
                    },
                    "content": {
                        "type": "string/object",
                        "description": "Message content, can be simple text (e.g., 'text Hello world!') or JSON formatted message",
                    },
                },
                example='/_send @1 json {"msgContent":{"type":"text","text":"Hello world!"}}',
                category="Messaging",
                api_prefix=True,
            ),
            "/_update_item": CommandInfo(
                name="/_update_item",
                description="Update the content of a previously sent message.",
                parameters={
                    "chatId": {
                        "type": "string",
                        "description": "The chat ID with prefix '@' for contacts or '#' for groups",
                    },
                    "itemId": {
                        "type": "string/integer",
                        "description": "The ID of the message to update",
                    },
                    "content": {
                        "type": "string/object",
                        "description": "The new message content, formatted as in /_send",
                    },
                },
                example='/_update_item @1 2 json {"type":"text","text":"Updated message"}',
                category="Messaging",
                api_prefix=True,
            ),
            "/_delete_item": CommandInfo(
                name="/_delete_item",
                description="Delete a message with optional broadcast to notify other users.",
                parameters={
                    "chatId": {
                        "type": "string",
                        "description": "The chat ID with prefix '@' for contacts or '#' for groups",
                    },
                    "itemId": {
                        "type": "string/integer",
                        "description": "The ID of the message to delete",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Delete mode, can be 'broadcast' to notify other users",
                    },
                },
                example="/_delete_item @1 2 broadcast",
                category="Messaging",
                api_prefix=True,
            ),
            "/_connect": CommandInfo(
                name="/_connect",
                description="Connect to another user using an invitation link or connection address.",
                parameters={
                    "link": {
                        "type": "string",
                        "description": "The invitation link or connection address",
                    }
                },
                example="/_connect smp://LcJUMfVhwD8yxjAiSaDzzGF3-kLG4Uh0Fl_ZIjrRwjI=@smp.example.com/contact#/?v=1-2&e=random_data",
                category="Contact Management",
                api_prefix=True,
            ),
            "/_accept": CommandInfo(
                name="/_accept",
                description="Accept a contact request from another user.",
                parameters={
                    "contactRequestId": {
                        "type": "integer",
                        "description": "The ID of the contact request to accept",
                    }
                },
                example="/_accept 1",
                category="Contact Management",
                api_prefix=True,
            ),
            "/_reject": CommandInfo(
                name="/_reject",
                description="Reject a contact request from another user.",
                parameters={
                    "contactRequestId": {
                        "type": "integer",
                        "description": "The ID of the contact request to reject",
                    }
                },
                example="/_reject 2",
                category="Contact Management",
                api_prefix=True,
            ),
            "/_group": CommandInfo(
                name="/_group",
                description="Create a new group chat with specified name and description.",
                parameters={
                    "profile": {
                        "type": "object",
                        "description": "Group profile information with displayName (required) and fullName (optional)",
                    }
                },
                example='/_group {"displayName":"Project Team","fullName":"Team for the XYZ project"}',
                category="Group Management",
                api_prefix=True,
            ),
            "/_add": CommandInfo(
                name="/_add",
                description="Add a contact to a group with optional role assignment.",
                parameters={
                    "groupId": {
                        "type": "string",
                        "description": "The group ID with prefix '#'",
                    },
                    "contactId": {
                        "type": "string/integer",
                        "description": "The contact ID to add",
                    },
                    "memberRole": {
                        "type": "string",
                        "description": "The role to assign to the new member (member, admin, owner)",
                    },
                },
                example="/_add #1 2 member",
                category="Group Management",
                api_prefix=True,
            ),
            "/_leave": CommandInfo(
                name="/_leave",
                description="Leave a group that you are a member of.",
                parameters={
                    "groupId": {
                        "type": "string",
                        "description": "The group ID with prefix '#'",
                    }
                },
                example="/_leave #1",
                category="Group Management",
                api_prefix=True,
            ),
            "/_members": CommandInfo(
                name="/_members",
                description="List all members of a group with their roles and profiles.",
                parameters={
                    "groupId": {
                        "type": "string",
                        "description": "The group ID with prefix '#'",
                    }
                },
                example="/_members #1",
                category="Group Management",
                api_prefix=True,
            ),
            "/version": CommandInfo(
                name="/version",
                description="Show version information for the SimpleX Chat server and libraries.",
                category="System",
            ),
        }

        self.commands.update(basic_commands)

    def extract_commands_from_controller(self):
        """Extract command types from Controller.hs"""
        if not self.controller_path:
            logger.warning(
                "Controller.hs path not provided. Skipping command extraction."
            )
            return

        logger.info(f"Extracting commands from {self.controller_path}")

        try:
            # Either open local file or fetch from URL
            if self.controller_path.startswith("http"):
                with urlopen(self.controller_path) as response:
                    controller_content = response.read().decode("utf-8")
            else:
                with open(self.controller_path, "r") as f:
                    controller_content = f.read()

            # Find the ChatCommand data type definition
            # Using a more robust pattern that looks for data ChatCommand and captures everything up to deriving (Show)
            command_def_match = re.search(
                r"data\s+ChatCommand\s*\n?\s*=\s*([\s\S]*?)(?:deriving\s*\([^)]*\))",
                controller_content,
            )

            if not command_def_match:
                logger.error("Could not find ChatCommand definition in Controller.hs")
                # Fallback to adding some basic commands
                self._add_fallback_commands()
                return

            command_def = command_def_match.group(1)

            # Extract commands from the definition - look for lines with | followed by identifier
            command_pattern = re.compile(
                r"^\s*\|\s*([A-Za-z0-9]+)(?:\s*{[^}]*}|\s+[^|\n]*)?", re.MULTILINE
            )
            commands = command_pattern.findall(command_def)

            if not commands:
                # Try alternate pattern without leading |
                command_pattern = re.compile(
                    r"^\s*([A-Za-z0-9]+)(?:\s*{[^}]*}|\s+[^|\n]*)?", re.MULTILINE
                )
                commands = command_pattern.findall(command_def)

            logger.info(f"Found {len(commands)} command variants in Controller.hs")

            # Process each command
            for cmd in commands:
                category = self._determine_category(cmd)
                api_prefix = cmd.startswith("API")
                command_name = self._derive_command_name(cmd)

                # Extract parameter information from the command definition if possible
                param_info = self._extract_param_info(cmd, controller_content)

                if command_name:
                    # If we already have this command with enhanced description, keep it
                    # but update any missing fields
                    if command_name in self.commands:
                        existing_cmd = self.commands[command_name]
                        existing_cmd.chat_command_variant = cmd
                        existing_cmd.api_prefix = api_prefix
                        if not existing_cmd.parameters and param_info:
                            existing_cmd.parameters = param_info
                    else:
                        description = self._generate_command_description(cmd)
                        self.commands[command_name] = CommandInfo(
                            name=command_name,
                            description=description,
                            category=category,
                            api_prefix=api_prefix,
                            chat_command_variant=cmd,
                            parameters=param_info or {},
                        )

        except Exception as e:
            logger.error(f"Error extracting commands from Controller.hs: {str(e)}")
            self._add_fallback_commands()

    def _extract_param_info(
        self, cmd_variant: str, controller_content: str
    ) -> Dict[str, Dict[str, str]]:
        """Extract parameter information for a command from Controller.hs"""
        param_info = {}

        try:
            # Look for the command data constructor pattern
            cmd_pattern = re.compile(rf"{cmd_variant}\s+{{([^}}]+)}}", re.MULTILINE)

            match = cmd_pattern.search(controller_content)
            if match:
                # Extract parameter fields from the data constructor
                param_text = match.group(1)
                param_lines = param_text.strip().split(",")

                for line in param_lines:
                    line = line.strip()
                    if "::" in line:
                        parts = line.split("::")
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            type_info = "::".join(parts[1:]).strip()

                            # Generate description based on type
                            if "Text" in type_info:
                                param_type = "string"
                            elif "Int" in type_info:
                                param_type = "integer"
                            elif "Bool" in type_info:
                                param_type = "boolean"
                            elif "Object" in type_info or "Map" in type_info:
                                param_type = "object"
                            elif "Array" in type_info or "[" in type_info:
                                param_type = "array"
                            else:
                                param_type = "any"

                            description = f"Parameter of type {type_info}"

                            param_info[name] = {
                                "type": param_type,
                                "description": description,
                            }

            return param_info

        except Exception as e:
            logger.warning(f"Error extracting parameters for {cmd_variant}: {e}")
            return {}

    def _generate_command_description(self, cmd_variant: str) -> str:
        """Generate a more descriptive command description based on the variant name"""
        # Extract words from CamelCase
        words = re.findall(r"[A-Z][a-z]*", cmd_variant)

        if not words:
            return f"Command from ChatCommand variant: {cmd_variant}"

        # If it starts with API, remove it for the description
        if words[0] == "API":
            words = words[1:]

        # Create a reasonable description from the words
        if len(words) >= 2:
            verb = words[0].lower()
            noun = " ".join([w.lower() for w in words[1:]])
            return f"{verb.capitalize()} {noun}"

        return f"Command from ChatCommand variant: {cmd_variant}"

    def _add_fallback_commands(self):
        """Add basic commands as fallback when extraction fails"""
        logger.info("Adding fallback commands")

        # Basic commands that should work in most SimpleX instances
        fallback_commands = [
            (
                "/u",
                "User Management",
                "Show the currently active user profile with details",
            ),
            (
                "/users",
                "User Management",
                "List all users (profiles) configured on this instance",
            ),
            (
                "/_create",
                "User Management",
                "Create a new user profile with specified details",
            ),
            (
                "/_user",
                "User Management",
                "Set a different user as the active user by ID",
            ),
            (
                "/_start",
                "Chat Management",
                "Start the chat system, enabling messaging capabilities",
            ),
            (
                "/_stop",
                "Chat Management",
                "Stop the chat system, disabling messaging capabilities",
            ),
            (
                "/_get chats",
                "Chat Management",
                "Get the list of all chats for the current user",
            ),
            (
                "/_get chat",
                "Chat Management",
                "Get messages for a specific chat with pagination",
            ),
            ("/_send", "Messaging", "Send a message to a chat (contact or group)"),
            (
                "/_connect",
                "Contact Management",
                "Connect to another user using an invitation link",
            ),
            (
                "/_accept",
                "Contact Management",
                "Accept a contact request from another user",
            ),
            (
                "/_reject",
                "Contact Management",
                "Reject a contact request from another user",
            ),
            (
                "/_group",
                "Group Management",
                "Create a new group chat with specified details",
            ),
            (
                "/_members",
                "Group Management",
                "List all members of a group with their roles",
            ),
            (
                "/_add",
                "Group Management",
                "Add a contact to a group with optional role",
            ),
            ("/_leave", "Group Management", "Leave a group that you are a member of"),
            ("/version", "System", "Show version information for SimpleX Chat"),
        ]

        for cmd, category, desc in fallback_commands:
            self.commands[cmd] = CommandInfo(
                name=cmd,
                description=desc,
                category=category,
                api_prefix=cmd.startswith("/_"),
            )

    def _determine_category(self, cmd_variant: str) -> str:
        """Determine the category of a command based on its name"""
        for category, cmd_list in self.command_categories.items():
            if cmd_variant in cmd_list:
                return category

        # Try to guess category based on command name
        if any(kw in cmd_variant for kw in ["User", "Profile"]):
            return "User Management"
        elif any(
            kw in cmd_variant for kw in ["Chat", "Message", "Send", "Delete", "Edit"]
        ):
            return "Messaging"
        elif any(
            kw in cmd_variant for kw in ["Contact", "Connect", "Accept", "Reject"]
        ):
            return "Contact Management"
        elif any(kw in cmd_variant for kw in ["Group", "Member", "Join", "Leave"]):
            return "Group Management"
        elif any(kw in cmd_variant for kw in ["File", "Image", "Receive", "Cancel"]):
            return "File Transfer"
        elif any(kw in cmd_variant for kw in ["Call", "Invitation", "Offer", "Answer"]):
            return "Call Management"
        elif any(kw in cmd_variant for kw in ["Network", "Server", "Config", "Status"]):
            return "Network & Settings"
        elif any(kw in cmd_variant for kw in ["Remote", "Host", "Ctrl"]):
            return "Remote Control"

        return "Uncategorized"

    def _derive_command_name(self, cmd_variant: str) -> Optional[str]:
        """Derive the actual command name from a ChatCommand variant"""
        # Enhanced mappings from variants to actual commands
        variant_to_cmd = {
            "ShowActiveUser": "/u",
            "ListUsers": "/users",
            "CreateActiveUser": "/_create user",
            "StartChat": "/_start",
            "APIStopChat": "/_stop",
            "APIGetChats": "/_get chats",
            "APIGetChat": "/_get chat",
            "SendMessage": "/_send",
            "SendCallInvitation": "/_call",
            "AcceptContact": "/_accept",
            "APIAddContact": "/_connect",
            "NewGroup": "/_group",
            "AddMember": "/_add",
            "APIUpdateProfile": "/_profile",
            "ShowProfile": "/_profile show",
            "APILeaveGroup": "/_leave",
            "ListMembers": "/_members",
            # Add more mappings as they're discovered
        }

        if cmd_variant in variant_to_cmd:
            return variant_to_cmd[cmd_variant]

        # For API variants, convert to lowercase with underscores
        if cmd_variant.startswith("API"):
            cmd_name = cmd_variant[3:]  # Remove "API" prefix
            cmd_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", cmd_name).lower()
            return f"/_{cmd_name}"

        # For non-API variants, try to convert to a reasonable command name
        if not cmd_variant.startswith("API"):
            # First word becomes the command, rest become parameters
            words = re.findall(r"[A-Z][a-z]*", cmd_variant)
            if words and len(words) >= 1:
                prefix = ""
                cmd_word = words[0].lower()

                # Check if this is likely an API command based on the variant
                if any(
                    api_word in cmd_variant
                    for api_word in ["Get", "Set", "Create", "Update", "Delete"]
                ):
                    prefix = "/_"

                return f"{prefix}{cmd_word}"

        return None

    def process_json_schema(self):
        """Process the JSON schema to understand message types"""
        if not self.schema_path:
            logger.warning("Schema path not provided. Skipping schema processing.")
            return

        logger.info(f"Processing JSON schema from {self.schema_path}")

        try:
            # Either open local file or fetch from URL
            if self.schema_path.startswith("http"):
                with urlopen(self.schema_path) as response:
                    schema_content = response.read().decode("utf-8")
                    schema = json.loads(schema_content)
            else:
                with open(self.schema_path, "r") as f:
                    schema = json.load(f)

            # Process definitions
            definitions = schema.get("definitions", {})
            for def_name, def_schema in definitions.items():
                comment = def_schema.get("metadata", {}).get("comment", "")
                description = f"Schema definition for {def_name}"
                if comment:
                    description += f": {comment}"

                self.schema_definitions[def_name] = SchemaInfo(
                    name=def_name,
                    schema=def_schema,
                    description=description,
                )

            # Process message types
            mapping = schema.get("mapping", {})
            for msg_type, msg_schema in mapping.items():
                response_name = msg_type.replace("x.", "")

                # Generate better description from the message type
                description = self._generate_response_description(msg_type)

                self.responses[response_name] = ResponseInfo(
                    name=response_name,
                    schema=msg_schema,
                    description=description,
                )

            logger.info(
                f"Processed {len(self.schema_definitions)} schema definitions and {len(self.responses)} message types"
            )

        except Exception as e:
            logger.error(f"Error processing JSON schema: {e}")

    def _generate_response_description(self, msg_type: str) -> str:
        """Generate a descriptive explanation of a response type"""
        # Extract the main type name without the x. prefix
        type_name = msg_type.replace("x.", "")

        # Split by dots to get components
        components = type_name.split(".")

        if len(components) == 1:
            return f"Response for {components[0]} operations"

        # Map common first components to descriptions
        component_map = {
            "contact": "Contact management",
            "info": "Information",
            "msg": "Message",
            "file": "File transfer",
            "direct": "Direct communication",
            "grp": "Group",
            "call": "Call",
            "ok": "Success confirmation",
        }

        # Build description based on components
        if components[0] in component_map:
            base_desc = component_map[components[0]]

            # Add more context based on additional components
            if len(components) > 1:
                subaction = components[1]
                if subaction == "new":
                    return f"{base_desc} creation response"
                elif subaction == "update":
                    return f"{base_desc} update response"
                elif subaction == "del":
                    return f"{base_desc} deletion response"
                elif subaction == "acpt":
                    return f"{base_desc} acceptance response"
                elif subaction == "inv":
                    return f"{base_desc} invitation response"
                elif subaction == "info":
                    return f"{base_desc} information response"
                elif subaction == "react":
                    return f"{base_desc} reaction response"
                else:
                    return f"{base_desc} {subaction} response"

            return f"{base_desc} response"

        return f"Message type: {msg_type}"

    async def setup_environment(self):
        """Create necessary resources for testing"""
        # Check for active user
        resp = await self.send_command("/u")
        if resp and "resp" in resp and resp["resp"].get("type") == "chatCmdError":
            # Create a user if none exists
            logger.info("No active user, creating one...")
            resp = await self.send_command(
                '/_create user {"profile":{"displayName":"DocBot","fullName":"Documentation Bot"},"sameServers":true,"pastTimestamp":false}'
            )

            if resp and "resp" in resp and resp["resp"].get("type") == "activeUser":
                user_id = resp["resp"]["user"].get("userId")
                if user_id:
                    self.active_user_id = user_id
                    self.resources["users"].append(user_id)
        elif resp and "resp" in resp and resp["resp"].get("type") == "activeUser":
            user_id = resp["resp"]["user"].get("userId")
            if user_id:
                self.active_user_id = user_id
                self.resources["users"].append(user_id)

        # Start chat
        await self.send_command("/_start subscribe=on expire=on")
        await asyncio.sleep(1)  # Give server time to process

    async def execute_test_commands(self):
        """Execute a sequence of commands to test the API"""
        logger.info("Executing test command sequence...")

        # List of commands to test
        test_commands = [
            # Basic user commands
            "/u",
            "/users",
            # Get the version information
            "/version",
            # Start chat system - retry with proper format if it fails
            "/_start",
            # Test chat commands
            "/_get chats",
            # Test creating/managing contacts and groups
            # These command formats have been adjusted based on observed errors
            f"/_create_user_address {self.active_user_id}"
            if self.active_user_id
            else None,
            f"/_show_user_address {self.active_user_id}"
            if self.active_user_id
            else None,
            '/_create_group {"displayName":"Test Group","fullName":"Test Group Description"}',
            # Try a few other commands
            "/help",
            "/?",
        ]

        # Filter out None commands
        test_commands = [cmd for cmd in test_commands if cmd is not None]

        # Execute each command and record responses
        for cmd in test_commands:
            response = await self.send_command(cmd)
            # Wait a bit between commands to avoid overwhelming the server
            await asyncio.sleep(0.2)

            # If we got an error for /_start, try alternative format
            if (
                cmd == "/_start"
                and response
                and "resp" in response
                and response["resp"].get("type") == "chatCmdError"
            ):
                alternative_cmd = "/_start subscribe=on expire=on xftp=on"
                logger.info(f"Trying alternative start command: {alternative_cmd}")
                await self.send_command(alternative_cmd)
                await asyncio.sleep(0.5)

        # More targeted testing: advanced commands
        await self.test_advanced_commands()

    async def test_advanced_commands(self):
        """Test more advanced commands for better documentation"""
        # Check if we have any groups now
        if self.resources["groups"]:
            group_id = self.resources["groups"][0]

            # Test group commands
            await self.send_command(f"/_members #{group_id}")
            await self.send_command(
                f'/_group_profile #{group_id} {{"displayName":"Updated Group","fullName":"Updated Description"}}'
            )
            await self.send_command(f"/_create_group_link #{group_id} member")

        # Check if we have any contacts
        if self.resources["contacts"]:
            contact_id = self.resources["contacts"][0]

            # Test contact/messaging commands
            await self.send_command(
                f'/_send @{contact_id} json [{{"msgContent":{{"type":"text","text":"Test message"}}}}]'
            )
            await asyncio.sleep(0.5)

            if self.resources["messages"]:
                msg_id = self.resources["messages"][0]
                await self.send_command(
                    f'/_update_item @{contact_id} {msg_id} json {{"type":"text","text":"Updated message"}}'
                )
                await self.send_command(
                    f"/_delete_item @{contact_id} {msg_id} broadcast"
                )

            await self.send_command(f"/_read_chat @{contact_id}")

        # Try creating a contact link
        if self.active_user_id:
            await self.send_command(f"/_create_contact_link")
            await self.send_command(f"/_show_contact_link")

        # Test some error cases deliberately to document error patterns
        await self.test_error_patterns()

    async def test_error_patterns(self):
        """Test some common error patterns to document them"""
        # Test trying to send a message without starting chat
        await self.send_command("/_stop")
        await asyncio.sleep(0.5)
        await self.send_command("/_send @1 text Test message")

        # Test invalid parameters
        await self.send_command("/_start")
        await asyncio.sleep(0.5)
        await self.send_command("/_user invalid")

        # Test nonexistent entities
        await self.send_command("/_get chat @999")
        await self.send_command("/_members #999")

        # Test malformed JSON
        await self.send_command('/_group {"incomplete')

        # Restore normal operation
        await self.send_command("/_start subscribe=on expire=on")

    def command_documentation(self, cmd_key: str) -> str:
        """Generate enhanced documentation for a specific command"""
        cmd_info = self.commands.get(cmd_key)
        if not cmd_info:
            return ""

        docs = [f"### `{cmd_info.name}`\n"]
        docs.append(f"{cmd_info.description}\n")

        # Parameters
        params = cmd_info.parameters
        if params:
            docs.append("**Parameters:**\n")
            for param_name, param_info in params.items():
                param_type = param_info.get("type", "any")
                param_desc = param_info.get("description", "")
                docs.append(f"- `{param_name}` ({param_type}): {param_desc}")
            docs.append("")

        # Example usage
        example = cmd_info.example or cmd_key
        docs.append("**Example Usage:**\n")
        docs.append("```json")
        docs.append(json.dumps({"corrId": "123", "cmd": example}, indent=2))
        docs.append("```\n")

        # Example responses
        responses = self.command_responses.get(cmd_key, [])
        if responses:
            docs.append("**Example Responses:**\n")
            for idx, response in enumerate(responses[:2]):  # Limit to 2 examples
                docs.append(f"Response {idx + 1}:\n")
                docs.append("```json")
                docs.append(json.dumps(response, indent=2))
                docs.append("```\n")

                # Extract response type if available
                if "resp" in response and "type" in response["resp"]:
                    resp_type = response["resp"]["type"]
                    docs.append(f"Response type: `{resp_type}`\n")
        else:
            docs.append(
                "*This command was not tested - no example responses available.*\n"
            )

        # Common errors and solutions
        error_patterns = cmd_info.error_patterns
        if error_patterns:
            docs.append("**Common Errors:**\n")
            for idx, error in enumerate(error_patterns[:2]):  # Limit to 2 examples
                error_type = error.get("type")
                error_data = error.get("data", {})

                if error_type == "error" and "errorType" in error_data:
                    sub_type = error_data["errorType"].get("type")
                    message = error_data["errorType"].get("message", "Unknown error")
                    docs.append(f"- `{sub_type}`: {message}")

                    # Add solution if we have a matching error in common_errors
                    for error_key, error_info in self.common_errors.items():
                        if (
                            error_info.error_type == sub_type
                            and message
                            and error_info.message in message
                        ):
                            docs.append(f"  - Cause: {error_info.cause}")
                            docs.append(f"  - Solution: {error_info.solution}")
                elif error_type == "errorStore":
                    store_error = error_data.get("storeError", {})
                    sub_type = store_error.get("type", "Unknown store error")
                    docs.append(f"- `{sub_type}`")

                    # Add solution if we have a matching error in common_errors
                    for error_key, error_info in self.common_errors.items():
                        if (
                            error_info.error_type == "errorStore"
                            and sub_type in error_info.message
                        ):
                            docs.append(f"  - Cause: {error_info.cause}")
                            docs.append(f"  - Solution: {error_info.solution}")
                else:
                    docs.append(f"- `{error_type}`: See response example for details")

            docs.append("")

        docs.append("---\n")
        return "\n".join(docs)

    def generate_markdown_docs(self) -> str:
        """Generate comprehensive markdown documentation"""
        docs = [
            "# SimpleX Chat WebSocket API Reference",
            "\n## Overview",
            "\nThe SimpleX Chat WebSocket API provides a bidirectional communication interface to the SimpleX Chat server.",
            "This API allows clients to interact with all SimpleX Chat features including user management, messaging, group chats, and file transfers.",
            "SimpleX Chat focuses on privacy and security - the WebSocket API maintains these guarantees while enabling automation and integration.",
            "\n## Connection",
            "\nConnect to the SimpleX Chat server using a WebSocket connection to the server's address and port:",
            "\n```",
            f"ws://host:port  (e.g., {self.url})",
            "```",
            "\nYou can run SimpleX Chat CLI in WebSocket server mode with:",
            "\n```bash",
            "simplex-chat -w 5226",
            "```",
            "\n## Message Format",
            "\nMessages sent to the server follow this format:",
            "\n```json",
            "{",
            '  "corrId": "123",  // Correlation ID to match responses with requests',
            '  "cmd": "/command [params]"  // Command string',
            "}",
            "```",
            "\nResponses from the server follow this format:",
            "\n```json",
            "{",
            '  "corrId": "123",  // Same correlation ID as the request',
            '  "resp": {',
            '    "type": "responseType",',
            "    // Additional response fields...",
            "  }",
            "}",
            "```",
            "\n## User Session Flow",
            "\nA typical session follows this pattern:",
            "\n1. Check for active user with `/u`",
            "2. Create user if needed with `/_create`",
            "3. Start chat system with `/_start subscribe=on expire=on`",
            "4. Perform actions (send messages, manage contacts, etc.)",
            "5. Stop chat system with `/_stop` when done",
            "\n## Error Handling",
            "\nError responses have the following structure:",
            "\n```json",
            "{",
            '  "corrId": "123",',
            '  "resp": {',
            '    "type": "chatCmdError",',
            '    "chatError": {',
            '      "type": "error",',
            '      "errorType": {',
            '        "type": "commandError",',
            '        "message": "Error details"',
            "      }",
            "    }",
            "  }",
            "}",
            "```",
            "\nCommon error types include:",
            "\n- `commandError`: Problems with command syntax or parameters",
            "- `errorStore`: Database or storage-related errors",
            "- `errorAgent`: Communication with the agent process failed",
            "- `errorChat`: Chat-related errors",
            "\nMost common causes of errors:",
            "\n1. Not starting chat with `/_start` before sending commands",
            "2. Invalid parameter format, especially with JSON objects",
            "3. Referencing entities (contacts, groups) that don't exist",
            "4. Insufficient permissions for the requested operation",
        ]

        # List all command categories first
        categories = set()
        for cmd_info in self.commands.values():
            categories.add(cmd_info.category)

        # Sort categories
        sorted_categories = sorted(categories)

        # Add a section for each category
        docs.append("\n## Command Categories")
        for category in sorted_categories:
            docs.append(f"\n### {category}")
            # Add a more descriptive explanation of the category
            if category == "User Management":
                docs.append(
                    "Commands for managing user profiles, identities, and preferences."
                )
            elif category == "Chat Management":
                docs.append(
                    "Commands for controlling the chat system and retrieving chat information."
                )
            elif category == "Messaging":
                docs.append("Commands for sending, editing, and deleting messages.")
            elif category == "Contact Management":
                docs.append(
                    "Commands for connecting with other users and managing contacts."
                )
            elif category == "Group Management":
                docs.append(
                    "Commands for creating and managing group chats and their members."
                )
            elif category == "File Transfer":
                docs.append("Commands for sending, receiving, and managing files.")
            elif category == "Call Management":
                docs.append(
                    "Commands for initiating and managing voice and video calls."
                )
            elif category == "Network & Settings":
                docs.append(
                    "Commands for configuring network settings and server connections."
                )
            elif category == "Remote Control":
                docs.append("Commands for remote control functionality.")
            else:
                docs.append(f"Commands for managing {category.lower()}.")

        # Group commands by category
        commands_by_category = {}
        for cmd_key, cmd_info in self.commands.items():
            if cmd_info.category not in commands_by_category:
                commands_by_category[cmd_info.category] = []
            commands_by_category[cmd_info.category].append(cmd_key)

        # Generate detailed command documentation by category
        docs.append("\n## Commands")

        for category in sorted_categories:
            docs.append(f"\n### {category} Commands")

            # Get commands in this category
            commands = commands_by_category.get(category, [])
            commands.sort()

            # Add documentation for each command
            for cmd in commands:
                cmd_docs = self.command_documentation(cmd)
                docs.append(cmd_docs)

        # Add a section for response types
        docs.append("\n## Response Types\n")

        # Collect all response types we've seen
        seen_response_types = set()
        for cmd_info in self.commands.values():
            seen_response_types.update(cmd_info.response_types)

        for resp_type in sorted(seen_response_types):
            docs.append(f"### `{resp_type}`\n")

            # Add description if available from schema
            schema_description = ""
            if resp_type in self.responses:
                schema_description = self.responses[resp_type].description
            else:
                # Try to generate a description from the name
                schema_description = self._generate_response_description(resp_type)

            docs.append(f"{schema_description}\n")

            # Show examples of this response type from our test data
            examples = []
            for cmd_responses in self.command_responses.values():
                for resp in cmd_responses:
                    if (
                        "resp" in resp
                        and "type" in resp["resp"]
                        and resp["resp"]["type"] == resp_type
                    ):
                        examples.append(resp)
                        if len(examples) >= 2:  # Limit to 2 examples
                            break
                if len(examples) >= 2:
                    break

            if examples:
                docs.append("**Examples:**\n")
                for idx, example in enumerate(examples):
                    docs.append(f"Example {idx + 1}:\n")
                    docs.append("```json")
                    docs.append(json.dumps(example, indent=2))
                    docs.append("```\n")
            else:
                docs.append("*No examples available for this response type.*\n")

            docs.append("---\n")

        # Document response types we've seen in schema but not in responses
        schema_response_types = set(self.responses.keys()) - seen_response_types
        if schema_response_types:
            docs.append("### Additional Response Types\n")
            docs.append(
                "The following response types are defined in the schema but were not observed during testing:\n"
            )

            for resp_type in sorted(schema_response_types):
                description = self.responses[resp_type].description
                docs.append(f"- `{resp_type}`: {description}")

            docs.append("\n---\n")

        # Add a section about schema definitions
        if self.schema_definitions:
            docs.append("\n## Schema Definitions\n")
            docs.append(
                "The following schema definitions are used in the SimpleX Chat Protocol:\n"
            )

            # Sort schema definitions by name
            sorted_defs = sorted(self.schema_definitions.items())

            # Add most important schema definitions first
            important_defs = ["profile", "msgContainer", "msgContent", "groupProfile"]
            for name in important_defs:
                if name in self.schema_definitions:
                    schema_info = self.schema_definitions[name]
                    docs.append(f"### `{name}`\n")
                    docs.append(f"{schema_info.description}\n")

                    # Show the schema structure
                    docs.append("**Schema:**\n")
                    docs.append("```json")
                    docs.append(json.dumps(schema_info.schema, indent=2))
                    docs.append("```\n")
                    docs.append("---\n")

            # Add remaining schema definitions
            for name, schema_info in sorted_defs:
                if name not in important_defs:
                    docs.append(f"### `{name}`\n")
                    docs.append(f"{schema_info.description}\n")

                    # Show the schema structure
                    docs.append("**Schema:**\n")
                    docs.append("```json")
                    docs.append(json.dumps(schema_info.schema, indent=2))
                    docs.append("```\n")
                    docs.append("---\n")

        # Add a section about CLI mapping
        docs.append("\n## CLI to WebSocket API Mapping\n")
        docs.append(
            "The SimpleX Chat CLI commands map to WebSocket API commands as follows:\n"
        )
        docs.append("| CLI Command | WebSocket API Command | Description |")
        docs.append("|------------|----------------------|-------------|")
        docs.append("| `/profile` | `/u` | Show current user profile |")
        docs.append("| `/p <name>` | `/_profile <userId> {...}` | Update profile |")
        docs.append(
            "| `/connect <link>` | `/_connect <link>` | Connect using invitation |"
        )
        docs.append(
            "| `/delete <contact>` | `/_delete @<contactId>` | Delete a contact |"
        )
        docs.append("| `/g <group>` | `/_group {...}` | Create a group |")
        docs.append(
            "| `/a <group> <contact>` | `/_add #<groupId> <contactId>` | Add member to group |"
        )
        docs.append("| `/l <group>` | `/_leave #<groupId>` | Leave a group |")
        docs.append(
            "| `/f <contact> <file>` | `/_send_file @<contactId> <filePath>` | Send a file |"
        )
        docs.append(
            "| `/m [contact/group]` | `/_get chat <contactId/groupId>` | View messages in a chat |"
        )

        # Add notes and best practices
        docs.append("\n## Notes and Best Practices\n")
        docs.append(
            "- **Sequence matters**: Always follow the correct command sequence (check user → start chat → perform actions)"
        )
        docs.append(
            "- **Command prerequisites**: Many commands require an active user and chat to be started first"
        )
        docs.append(
            "- **ID formats**: IDs are numeric and are prefixed with @ for contacts and # for groups in chat references"
        )
        docs.append(
            "- **Error handling**: Implement proper error handling for chatCmdError responses"
        )
        docs.append(
            "- **JSON formatting**: Make sure to properly escape JSON parameters in commands"
        )
        docs.append(
            "- **Correlation IDs**: Use unique correlation IDs for each command to track responses"
        )
        docs.append(
            "- **Connection reliability**: Consider implementing reconnection logic for long-running applications"
        )
        docs.append(
            "- **Command rate**: Don't send commands too quickly; allow time for server processing"
        )
        docs.append(
            "- **State management**: The WebSocket connection is stateful; maintain awareness of current state"
        )
        docs.append(
            "- **Security**: Always validate and sanitize inputs, especially when processing user-provided content"
        )

        # Add an appendix with common error patterns and solutions
        docs.append("\n## Common Error Patterns and Solutions\n")

        docs.append("| Error Type | Common Message | Cause | Solution |")
        docs.append("|------------|----------------|-------|----------|")

        for error_key, error_info in self.common_errors.items():
            docs.append(
                f"| `{error_info.error_type}` | {error_info.message} | {error_info.cause} | {error_info.solution} |"
            )

        # Add documentation contributors section
        docs.append("\n## Documentation Contributors\n")
        docs.append(
            "This documentation was automatically generated by SimpleX Chat WebSocket API Documentation Generator.\n"
        )
        docs.append(
            "To contribute to this documentation, you can enhance the script that generates it or submit pull requests for manual improvements.\n"
        )

        return "\n".join(docs)

    async def run_documentation_process(self):
        """Run the full documentation process"""
        # Extract commands from Controller.hs
        self.extract_commands_from_controller()

        # Process JSON schema
        self.process_json_schema()

        # Connect to the server
        connected = await self.connect()
        if not connected:
            logger.error(
                "Failed to connect to the server. Documentation will be limited."
            )
            return self.generate_markdown_docs()

        try:
            # Setup test environment
            await self.setup_environment()

            # Execute test commands
            await self.execute_test_commands()

            # Generate documentation
            docs = self.generate_markdown_docs()

            # Write to file
            docs_file = "simplex_api_reference.md"
            with open(docs_file, "w") as f:
                f.write(docs)

            logger.info(f"Documentation generated and saved to {docs_file}")
            return docs

        finally:
            # Close connection
            await self.close()


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SimpleX Chat WebSocket API Documentation Generator"
    )
    parser.add_argument(
        "--url",
        default="ws://localhost:5226",
        help="WebSocket URL of the SimpleX Chat server",
    )
    parser.add_argument(
        "--controller",
        default="https://raw.githubusercontent.com/simplex-chat/simplex-chat/refs/heads/stable/src/Simplex/Chat/Controller.hs",
        help="Path or URL to Controller.hs",
    )
    parser.add_argument(
        "--schema",
        default="https://raw.githubusercontent.com/simplex-chat/simplex-chat/refs/heads/stable/docs/protocol/simplex-chat.schema.json",
        help="Path or URL to simplex-chat.schema.json",
    )
    parser.add_argument(
        "--output",
        default="simplex_api_reference.md",
        help="Output file path for the documentation",
    )

    args = parser.parse_args()

    # Create the documenter
    documenter = SimpleXAPIDocumenter(
        url=args.url, controller_path=args.controller, schema_path=args.schema
    )

    # Run the documentation process
    docs = await documenter.run_documentation_process()

    # Write to specified output file
    with open(args.output, "w") as f:
        f.write(docs)

    logger.info(f"Documentation saved to {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
