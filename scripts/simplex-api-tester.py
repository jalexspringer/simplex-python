#!/usr/bin/env python3
"""
SimpleX WebSocket API Comprehensive Test Script

This script systematically tests all SimpleX WebSocket API commands and logs their responses
to provide comprehensive documentation of the API behavior and response formats.

Usage:
    python simplex_api_tester.py [--bot1-port PORT] [--bot2-port PORT] [--output OUTPUT_FILE]

Arguments:
    --bot1-port PORT     Port for BOT1 (default: 5225)
    --bot2-port PORT     Port for BOT2 (default: 5226)
    --output FILE        Output file path (default: test_results/simplex_api_test_results_TIMESTAMP.md)
    --help               Show this help message and exit

Environment:
    - Requires Python 3.8+ with asyncio and websockets
    - Assumes two SimpleX chat instances running (default ports 5225 for BOT1 and 5226 for BOT2)
    - Assumes the bots are already connected to each other

Installation:
    pip install websockets

Example:
    # Start SimpleX chat instances in separate terminals:
    # Terminal 1: ./simplex-chat -p 5225 -d bot1
    # Terminal 2: ./simplex-chat -p 5226 -d bot2

    # Then run the script:
    python simplex_api_tester.py

Output:
    The script generates a comprehensive Markdown file documenting all tested commands
    and their responses. This file can be viewed in any Markdown viewer or editor.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

import websockets


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("simplex_tester")

# Output file settings
OUTPUT_DIR = "test_results"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"simplex_api_test_results_{TIMESTAMP}.md")

# SimpleX WebSocket server settings
BOT1_WS_URL = "ws://localhost:5225/"
BOT2_WS_URL = "ws://localhost:5226/"


class SimplexAPITester:
    """Tests the SimpleX WebSocket API comprehensively and documents responses."""

    def __init__(self, bot1_url: str, bot2_url: str, output_file: str):
        self.bot1_url = bot1_url
        self.bot2_url = bot2_url
        self.output_file = output_file
        self.bot1_conn = None
        self.bot2_conn = None
        self.commands_map = {}
        self.results = []
        self.corr_id = 0
        self.contact_id = None  # Will store contactId for BOT2 in BOT1's context
        self.group_id = None  # Will store groupId created during testing

    async def connect(self):
        """Connect to both SimpleX WebSocket servers."""
        logger.info(f"Connecting to BOT1 at {self.bot1_url}")
        self.bot1_conn = await websockets.connect(self.bot1_url)
        logger.info(f"Connecting to BOT2 at {self.bot2_url}")
        self.bot2_conn = await websockets.connect(self.bot2_url)
        logger.info("Connected to both servers")

    async def disconnect(self):
        """Disconnect from both SimpleX WebSocket servers."""
        if self.bot1_conn:
            await self.bot1_conn.close()
        if self.bot2_conn:
            await self.bot2_conn.close()
        logger.info("Disconnected from both servers")

    async def send_command(
        self, conn, cmd: str, expect_response: bool = True, timeout: float = 5.0
    ) -> Dict[str, Any]:
        """
        Send a command to the specified WebSocket connection and get the response.

        Args:
            conn: WebSocket connection
            cmd: Command string to send
            expect_response: Whether to wait for a response
            timeout: Timeout in seconds for the response

        Returns:
            The response JSON object
        """
        self.corr_id += 1
        corr_id = str(self.corr_id)

        request = {"corrId": corr_id, "cmd": cmd}

        logger.debug(f"Sending command: {cmd} (corrId: {corr_id})")
        await conn.send(json.dumps(request))

        if expect_response:
            try:
                response_text = await asyncio.wait_for(conn.recv(), timeout=timeout)
                response = json.loads(response_text)
                logger.debug(f"Received response for corrId {corr_id}")
                return response
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for response to command: {cmd}")
                return {"error": "Timeout waiting for response"}
            except Exception as e:
                logger.error(f"Error receiving response: {str(e)}")
                return {"error": str(e)}

        return {"info": "No response expected"}

    async def test_command(
        self, conn, description: str, cmd: str, expect_response: bool = True
    ) -> Tuple[Dict[str, Any], str]:
        """
        Test a command and format the results.

        Args:
            conn: WebSocket connection
            description: Description of the command
            cmd: Command string to send
            expect_response: Whether to wait for a response

        Returns:
            Tuple of (response, formatted result)
        """
        logger.info(f"Testing command: {cmd}")

        try:
            response = await self.send_command(conn, cmd, expect_response)

            # Check for error in response
            is_error = False
            error_message = ""

            if "error" in response:
                is_error = True
                error_message = response.get("error", "Unknown error")
            elif (
                "resp" in response
                and response.get("resp", {}).get("type") == "chatCmdError"
            ):
                is_error = True
                error_info = response.get("resp", {}).get("chatError", {})
                error_message = f"Error type: {error_info.get('type', 'unknown')}"

            # Format the result with command details
            result = f"### {description}\n\n"

            # Add command details
            result += f"**Command:** `{cmd}`\n\n"

            # Add command format description based on the command
            if cmd.startswith("/_profile"):
                result += "**Format:** `/_profile userId profileJson`\n\n"
                result += "Updates the user's profile with new display name, full name, and image.\n\n"
            elif cmd.startswith("/_send"):
                result += "**Format:** `/_send chatType+chatId json messageArray`\n\n"
                result += "Sends one or more messages to a chat. Each message in the array can have different content types.\n\n"
            elif cmd.startswith("/_get chat"):
                result += (
                    "**Format:** `/_get chat chatType+chatId [pagination] [search]`\n\n"
                )
                result += "Gets chat history with optional pagination and search parameters.\n\n"
            elif cmd.startswith("/_group_profile"):
                result += "**Format:** `/_group_profile #groupId groupProfileJson`\n\n"
                result += "Updates a group's profile with new display name, full name, and preferences.\n\n"
            elif cmd.startswith("/group"):
                result += "**Format:** `/group displayName fullName image`\n\n"
                result += "Creates a new group with the specified display name, full name, and image.\n\n"

            # Add status (success/error)
            if is_error:
                result += "**Status:** ❌ Error\n\n"
                result += f"**Error Message:** {error_message}\n\n"
            else:
                result += "**Status:** ✅ Success\n\n"

            # Add response
            result += (
                f"**Response:**\n```json\n{json.dumps(response, indent=2)}\n```\n\n"
            )

            # Add response type analysis for successful commands
            if not is_error and "resp" in response:
                resp_type = response.get("resp", {}).get("type")
                if resp_type:
                    result += f"**Response Type:** `{resp_type}`\n\n"

                    # Add specific information based on response type
                    if resp_type == "cmdOk":
                        result += "Command executed successfully with no specific return data.\n\n"
                    elif resp_type == "activeUser":
                        user_id = response.get("resp", {}).get("user", {}).get("userId")
                        display_name = (
                            response.get("resp", {})
                            .get("user", {})
                            .get("localDisplayName")
                        )
                        result += f"Active user information returned (userId: {user_id}, displayName: {display_name}).\n\n"
                    elif resp_type == "userContactLink":
                        result += "User's contact link information returned.\n\n"
                    elif resp_type == "chat":
                        chat_items_count = len(
                            response.get("resp", {}).get("chatItems", [])
                        )
                        result += f"Chat information returned with {chat_items_count} messages.\n\n"
                    elif resp_type == "groupCreated":
                        group_id = (
                            response.get("resp", {}).get("groupInfo", {}).get("groupId")
                        )
                        group_name = (
                            response.get("resp", {})
                            .get("groupInfo", {})
                            .get("localDisplayName")
                        )
                        result += f"Group created successfully (groupId: {group_id}, name: {group_name}).\n\n"

            return response, result

        except Exception as e:
            logger.error(f"Error testing command: {cmd} - {str(e)}")

            # Format error result
            result = (
                f"### {description}\n\n"
                f"**Command:** `{cmd}`\n\n"
                f"**Status:** ❌ Error\n\n"
                f"**Error:** {str(e)}\n\n"
            )

            return {"error": str(e)}, result

    async def find_contact_id(self):
        """Find the contact ID for BOT2 in BOT1's context."""
        response, _ = await self.test_command(
            self.bot1_conn, "Getting chats to find contactId", "/chats"
        )

        try:
            chats = response.get("resp", {}).get("chats", [])
            for chat in chats:
                chat_info = chat.get("chatInfo", {})
                if chat_info.get("type") == "direct":
                    contact = chat_info.get("contact", {})
                    if contact.get("localDisplayName") == "BOT2":
                        self.contact_id = contact.get("contactId")
                        logger.info(f"Found BOT2 contactId: {self.contact_id}")
                        return self.contact_id
        except Exception as e:
            logger.error(f"Error finding contactId: {str(e)}")

        logger.warning("Could not find contactId for BOT2")
        return None

    def write_to_file(self, results: List[str]):
        """Write test results to the output file."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        with open(self.output_file, "w") as f:
            f.write("# SimpleX WebSocket API Test Results\n\n")
            f.write(f"Test date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Overview\n\n")
            f.write(
                "This document contains the results of testing various SimpleX WebSocket API commands. "
            )
            f.write(
                "Each section contains different categories of commands and their respective responses.\n\n"
            )

            f.write("### Table of Contents\n\n")
            f.write("- [User Commands](#user-commands)\n")
            f.write("- [Profile Commands](#profile-commands)\n")
            f.write("- [Address Commands](#address-commands)\n")
            f.write("- [Chat Commands](#chat-commands)\n")
            f.write("- [Group Commands](#group-commands)\n")
            f.write("- [Contact Commands](#contact-commands)\n")
            f.write("- [Message Commands](#message-commands)\n")
            f.write("- [Server Protocol Commands](#server-protocol-commands)\n")
            f.write("- [Database Commands](#database-commands)\n")
            f.write("- [File Commands](#file-commands)\n")
            f.write("- [Miscellaneous Commands](#miscellaneous-commands)\n\n")

            f.write("### Request Format\n\n")
            f.write(
                "All commands are sent as WebSocket messages with the following JSON format:\n\n"
            )
            f.write("```json\n")
            f.write("{\n")
            f.write('  "corrId": "123",\n')
            f.write('  "cmd": "command string"\n')
            f.write("}\n")
            f.write("```\n\n")

            f.write("Where:\n")
            f.write("- `corrId`: A correlation ID to match responses to requests\n")
            f.write("- `cmd`: The command string to execute\n\n")

            f.write("### Response Format\n\n")
            f.write("Responses are also JSON objects with the following structure:\n\n")
            f.write("```json\n")
            f.write("{\n")
            f.write('  "corrId": "123",\n')
            f.write('  "resp": {\n')
            f.write('    "type": "responseType",\n')
            f.write("    ...\n")
            f.write("  }\n")
            f.write("}\n")
            f.write("```\n\n")

            f.write("Where:\n")
            f.write("- `corrId`: The correlation ID from the request\n")
            f.write(
                "- `resp`: The response object containing various fields depending on the command\n\n"
            )

            for result in results:
                f.write(result)

            f.write("\n## Summary\n\n")
            f.write(
                "This document covers the most commonly used SimpleX WebSocket API commands. "
            )
            f.write(
                "For complete details, refer to the official SimpleX documentation or the "
            )
            f.write("source code of the SimpleX Chat application.\n\n")

            f.write("### Notes on Response Types\n\n")
            f.write(
                "- `cmdOk`: Indicates the command was executed successfully with no specific return data\n"
            )
            f.write(
                "- `activeUser`: Contains information about the currently active user\n"
            )
            f.write("- `usersList`: Contains a list of all users\n")
            f.write("- `userContactLink`: Contains the contact link for a user\n")
            f.write("- `chats`: Contains a list of all chats\n")
            f.write("- `chat`: Contains information about a specific chat\n")
            f.write(
                "- `chatCmdError`: Indicates an error occurred when executing the command\n"
            )
            f.write(
                "- `groupCreated`: Contains information about a newly created group\n"
            )
            f.write("- `userServers`: Contains information about the user's servers\n")

        logger.info(f"Results written to {self.output_file}")

    async def run_tests(self):
        """Run all SimpleX WebSocket API tests."""
        logger.info("Starting SimpleX WebSocket API tests")

        try:
            await self.connect()
            results = []

            # First find the contactId for BOT2 in BOT1's context
            await self.find_contact_id()

            # ==================== USER COMMANDS ====================
            section_header = "\n## User Commands\n\n"
            results.append(section_header)

            response, result = await self.test_command(
                self.bot1_conn, "Show Active User", "/u"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "List Users", "/users"
            )
            results.append(result)

            # Create a new user (will likely fail in non-GUI mode, but testing the command format)
            response, result = await self.test_command(
                self.bot1_conn,
                "Create Active User",
                f"/_create user {json.dumps({'profile': {'displayName': 'TEST_USER', 'fullName': 'Test User'}, 'sameServers': True, 'pastTimestamp': False})}",
            )
            results.append(result)

            # Hide/Unhide user (test on userId 1, which should exist)
            response, result = await self.test_command(
                self.bot1_conn, "Hide User", '/_hide user 1 "password"'
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Unhide User", '/_unhide user 1 "password"'
            )
            results.append(result)

            # Mute/Unmute user
            response, result = await self.test_command(
                self.bot1_conn, "Mute User", "/_mute user 1"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Unmute User", "/_unmute user 1"
            )
            results.append(result)

            # Set active user
            response, result = await self.test_command(
                self.bot1_conn, "Set Active User", "/_user 1"
            )
            results.append(result)

            # ==================== PROFILE COMMANDS ====================
            section_header = "\n## Profile Commands\n\n"
            results.append(section_header)

            response, result = await self.test_command(
                self.bot1_conn,
                "Update Profile",
                f"/_profile 1 {json.dumps({'displayName': 'BOT1_UPDATED', 'fullName': 'Bot One Updated', 'image': ''})}",
            )
            results.append(result)

            # ==================== ADDRESS COMMANDS ====================
            section_header = "\n## Address Commands\n\n"
            results.append(section_header)

            # Create my address
            response, result = await self.test_command(
                self.bot1_conn, "Create My Address", "/_address 1"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Show My Address", "/show_address"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Set Profile Address (enable)", "/profile_address on"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Set Profile Address (disable)", "/profile_address off"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Address Auto Accept", "/auto_accept off"
            )
            results.append(result)

            # Shorthand versions of address commands
            response, result = await self.test_command(
                self.bot1_conn, "Show My Address (shorthand)", "/sa"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn,
                "Create My Address (API version)",
                "/_address 1 short=on",
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Delete My Address", "/_delete_address 1"
            )
            results.append(result)

            # ==================== CHAT COMMANDS ====================
            section_header = "\n## Chat Commands\n\n"
            results.append(section_header)

            # Start/stop chat
            response, result = await self.test_command(
                self.bot1_conn, "Start Chat", "/_start subscribe=on expire=on"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Get Chats", "/chats"
            )
            results.append(result)

            if self.contact_id:
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Get Chat with Contact",
                    "/_get chat @BOT2",
                )
                results.append(result)

                # Get chat with pagination
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Get Chat with Pagination",
                    "/_get chat @BOT2 count=10",
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn,
                    "Mark Chat as Read",
                    f"/_read chat @{self.contact_id}",
                )
                results.append(result)

                # Clear chat
                response, result = await self.test_command(
                    self.bot1_conn, "Clear Chat", f"/_clear chat @{self.contact_id}"
                )
                results.append(result)

            # ==================== GROUP COMMANDS ====================
            section_header = "\n## Group Commands\n\n"
            results.append(section_header)

            response, result = await self.test_command(
                self.bot1_conn,
                "Create Group",
                "/group Test API Group Testing SimpleX WebSocket API None",
            )
            results.append(result)

            # Extract groupId from response
            try:
                group_info = response.get("resp", {}).get("groupInfo", {})
                self.group_id = group_info.get("groupId")
                logger.info(f"Created group with groupId: {self.group_id}")
            except Exception as e:
                logger.error(f"Could not extract groupId: {str(e)}")

            response, result = await self.test_command(
                self.bot1_conn,
                "List Groups",
                "/groups",
            )
            results.append(result)

            if self.group_id:
                response, result = await self.test_command(
                    self.bot1_conn, "List Group Members", f"/_members #{self.group_id}"
                )
                results.append(result)

                # Update group profile
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Update Group Profile",
                    f"/_group_profile #{self.group_id} {json.dumps({'displayName': 'Updated API Group', 'fullName': 'Updated SimpleX WebSocket API', 'groupPreferences': {'directMessages': {'enable': 'on'}, 'history': {'enable': 'on'}}})}",
                )
                results.append(result)

                # Add member (will try to add BOT2 to the group)
                if self.contact_id:
                    response, result = await self.test_command(
                        self.bot1_conn,
                        "Add Member to Group",
                        f"/_add #{self.group_id} {self.contact_id} member",
                    )
                    results.append(result)

                # Group links
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Create Group Link",
                    f"/_create link #{self.group_id} member",
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn,
                    "Change Group Link Role",
                    f"/_set link role #{self.group_id} admin",
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn, "Get Group Link", f"/_get link #{self.group_id}"
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn,
                    "Delete Group Link",
                    f"/_delete link #{self.group_id}",
                )
                results.append(result)

                # Group member info (should have at least owner)
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Group Member Info",
                    f"/_info #{self.group_id} 1",  # Assuming owner has memberId 1
                )
                results.append(result)

                # Leave group (commented out to maintain the group for other tests)
                # response, result = await self.test_command(
                #     self.bot1_conn,
                #     "Leave Group",
                #     f"/_leave #{self.group_id}"
                # )
                # results.append(result)

            # ==================== CONTACT COMMANDS ====================
            section_header = "\n## Contact Commands\n\n"
            results.append(section_header)

            # Contact commands
            if self.contact_id:
                response, result = await self.test_command(
                    self.bot1_conn, "Contact Info", f"/_info @{self.contact_id}"
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn,
                    "Set Contact Alias",
                    f"/_set alias @{self.contact_id} BOT2_ALIAS",
                )
                results.append(result)

                response, result = await self.test_command(
                    self.bot1_conn,
                    "Get Contact Connection Code",
                    f"/_get code @{self.contact_id}",
                )
                results.append(result)

                # Verify contact (may fail if no connection code)
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Verify Contact",
                    f"/_verify code @{self.contact_id}",
                )
                results.append(result)

                # List contacts
                response, result = await self.test_command(
                    self.bot1_conn, "List Contacts", "/_contacts 1"
                )
                results.append(result)

                # Get queue info
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Contact Queue Info",
                    f"/_queue info @{self.contact_id}",
                )
                results.append(result)

            # ==================== MESSAGE COMMANDS ====================
            section_header = "\n## Message Commands\n\n"
            results.append(section_header)

            # Send different types of messages
            if self.contact_id:
                # Send text message
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Send Text Message",
                    f'/_send @{self.contact_id} json [{{"msgContent": {{"text": "Test message from API", "type": "text"}}}}]',
                )
                results.append(result)

                # Get message ID from response to update/delete it later
                message_id = None
                try:
                    chat_items = response.get("resp", {}).get("chatItems", [])
                    if chat_items:
                        message_id = chat_items[0].get("meta", {}).get("itemId")
                        logger.info(f"Sent message with itemId: {message_id}")
                except Exception as e:
                    logger.error(f"Could not extract message itemId: {str(e)}")

                # Send message with multiple parts
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Send Multi-Part Message",
                    f'/_send @{self.contact_id} json [{{"msgContent": {{"text": "First part", "type": "text"}}}}, {{"msgContent": {{"text": "Second part", "type": "text"}}}}]',
                )
                results.append(result)

                # Send message with formatting (will be rendered as markdown)
                response, result = await self.test_command(
                    self.bot1_conn,
                    "Send Formatted Message",
                    f'/_send @{self.contact_id} json [{{"msgContent": {{"text": "# Heading\\n**Bold text** and *italic text*\\n```\\ncode block\\n```", "type": "text"}}}}]',
                )
                results.append(result)

                # Update message if we have a message ID
                if message_id:
                    response, result = await self.test_command(
                        self.bot1_conn,
                        "Update Message",
                        f'/_update item @{self.contact_id} {message_id} live=off json {{"text": "Updated message", "type": "text"}}',
                    )
                    results.append(result)

                    # Delete message
                    response, result = await self.test_command(
                        self.bot1_conn,
                        "Delete Message",
                        f"/_delete item @{self.contact_id} {message_id} internal",
                    )
                    results.append(result)

            # ==================== SERVER PROTOCOL COMMANDS ====================
            section_header = "\n## Server Protocol Commands\n\n"
            results.append(section_header)

            response, result = await self.test_command(
                self.bot1_conn, "Get SMP Servers", "/smp"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Get XFTP Servers", "/xftp"
            )
            results.append(result)

            # Test specific server (will likely fail unless server exists)
            response, result = await self.test_command(
                self.bot1_conn,
                "Test Server",
                "/_server test 1 smp://u2dS9sG8nMNURyZwqASV4yROM28Er0luVTx5X1CsMrU=@smp4.simplex.im",
            )
            results.append(result)

            # Get user servers
            response, result = await self.test_command(
                self.bot1_conn, "Get User Servers", "/_servers 1"
            )
            results.append(result)

            # ==================== DATABASE COMMANDS ====================
            section_header = "\n## Database Commands\n\n"
            results.append(section_header)

            # Export archive (commented out to avoid changing state)
            # export_config = {
            #     "filePath": "/tmp/simplex_export.zip",
            #     "includeMedia": True,
            #     "password": "test",
            # }
            # response, result = await self.test_command(
            #     self.bot1_conn,
            #     "Export Archive",
            #     f"/_db export {json.dumps(export_config)}"
            # )
            # results.append(result)

            # ==================== FILE COMMANDS ====================
            section_header = "\n## File Commands\n\n"
            results.append(section_header)

            # Create temp directory
            temp_folder = "/tmp/simplex_test"
            os.makedirs(temp_folder, exist_ok=True)

            response, result = await self.test_command(
                self.bot1_conn, "Set Temp Folder", f"/_temp_folder {temp_folder}"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Set Files Folder", f"/_files_folder {temp_folder}"
            )
            results.append(result)

            # Set incognito mode
            response, result = await self.test_command(
                self.bot1_conn, "Set Incognito Mode", "/incognito on"
            )
            results.append(result)

            response, result = await self.test_command(
                self.bot1_conn, "Disable Incognito Mode", "/incognito off"
            )
            results.append(result)

            # ==================== MISCELLANEOUS COMMANDS ====================
            section_header = "\n## Miscellaneous Commands\n\n"
            results.append(section_header)

            # Version command
            response, result = await self.test_command(
                self.bot1_conn, "Show Version", "/version"
            )
            results.append(result)

            # Check chat running
            response, result = await self.test_command(
                self.bot1_conn, "Check Chat Running", "/_check running"
            )
            results.append(result)

            # Network config
            response, result = await self.test_command(
                self.bot1_conn, "Get Network Config", "/network"
            )
            results.append(result)

            # Get network statuses
            response, result = await self.test_command(
                self.bot1_conn, "Get Network Statuses", "/_network_statuses"
            )
            results.append(result)

            # Write results to file
            self.write_to_file(results)

        except Exception as e:
            logger.error(f"Error during tests: {str(e)}")
        finally:
            await self.disconnect()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SimpleX WebSocket API Tester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--bot1-port", type=int, default=5225, help="Port for BOT1 (default: 5225)"
    )

    parser.add_argument(
        "--bot2-port", type=int, default=5226, help="Port for BOT2 (default: 5226)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=f"Output file path (default: {OUTPUT_FILE})",
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Configure URLs based on args
    bot1_url = f"ws://localhost:{args.bot1_port}/"
    bot2_url = f"ws://localhost:{args.bot2_port}/"

    # Use custom output file if provided
    output_file = args.output if args.output else OUTPUT_FILE

    print("Testing SimpleX WebSocket API")
    print(f"  BOT1 URL: {bot1_url}")
    print(f"  BOT2 URL: {bot2_url}")
    print(f"  Output file: {output_file}")
    print()

    try:
        tester = SimplexAPITester(bot1_url, bot2_url, output_file)
        await tester.run_tests()
        print()
        print(f"Testing complete! Results written to: {output_file}")
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTesting interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)
