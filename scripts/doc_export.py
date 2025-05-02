import json


def generate_markdown_docs(self) -> str:
    """Generate comprehensive markdown documentation"""
    docs = [
        "# SimpleX Chat WebSocket API Reference",
        "\n## Overview",
        "\nThe SimpleX Chat WebSocket API provides a bidirectional communication interface to the SimpleX Chat server.",
        "This API allows clients to interact with all SimpleX Chat features including user management, messaging, group chats, and file transfers.",
        "\n## Connection",
        "\nConnect to the SimpleX Chat server using a WebSocket connection to the server's address and port:",
        "\n```",
        f"ws://host:port  (e.g., {self.url})",
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
        "3. Start chat system with `/_start`",
        "4. Perform actions (send messages, manage contacts, etc.)",
        "5. Stop chat system with `/_stop` when done",
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
            cmd_info = self.commands.get(cmd)
            if not cmd_info:
                continue

            docs.append(f"\n#### `{cmd_info.name}`")
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
            example = cmd_info.example or cmd
            docs.append("**Example Usage:**\n")
            docs.append("```json")
            docs.append(json.dumps({"corrId": "123", "cmd": example}, indent=2))
            docs.append("```\n")

            # Example responses
            responses = self.command_responses.get(cmd, [])
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

            docs.append("---")

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

    # Add a section about schema definitions
    if self.schema_definitions:
        docs.append("\n## Schema Definitions\n")
        docs.append(
            "The following schema definitions are used in the SimpleX Chat Protocol:\n"
        )

        for name, schema_info in sorted(self.schema_definitions.items()):
            docs.append(f"### `{name}`\n")
            docs.append(f"{schema_info.description}\n")

            # Show the schema structure
            docs.append("**Schema:**\n")
            docs.append("```json")
            docs.append(json.dumps(schema_info.schema, indent=2))
            docs.append("```\n")
            docs.append("---\n")

    # Add a section about command line interface mapping
    docs.append("\n## CLI to WebSocket API Mapping\n")
    docs.append(
        "The SimpleX Chat CLI commands map to WebSocket API commands as follows:\n"
    )
    docs.append("| CLI Command | WebSocket API Command | Description |")
    docs.append("|------------|----------------------|-------------|")
    docs.append("| `/profile` | `/u` | Show current user profile |")
    docs.append("| `/p <name>` | `/_profile <userId> {...}` | Update profile |")
    docs.append("| `/connect <link>` | `/_connect <link>` | Connect using invitation |")
    docs.append("| `/delete <contact>` | `/_delete @<contactId>` | Delete a contact |")
    docs.append("| `/g <group>` | `/_group {...}` | Create a group |")
    docs.append(
        "| `/a <group> <contact>` | `/_add #<groupId> <contactId>` | Add member to group |"
    )
    docs.append("| `/l <group>` | `/_leave #<groupId>` | Leave a group |")

    # Add notes and best practices
    docs.append("\n## Notes and Best Practices\n")
    docs.append(
        "- Commands often require an active user - call `/u` to check and `/_create` to create one if needed"
    )
    docs.append(
        "- Many commands require chat to be started - call `/_start` before using most functionality"
    )
    docs.append(
        "- IDs are numeric and are prefixed with @ for contacts and # for groups in chat references"
    )
    docs.append(
        "- Error handling: watch for `chatCmdError` response types which indicate command errors"
    )
    docs.append(
        "- In the API, users are called 'users' while the CLI refers to them as 'profiles'"
    )
    docs.append(
        "- All WebSocket messages must include a unique `corrId` (correlation ID) property"
    )
    docs.append(
        "- Send one command at a time and wait for its response before sending another"
    )
    docs.append(
        "- The WebSocket connection is stateful - commands build on previous commands"
    )

    return "\n".join(docs)
