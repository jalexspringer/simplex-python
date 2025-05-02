"""
Command formatting utilities for Simplex protocol.

"""

from typing import Any, Dict, Optional, Union, TypedDict
import json
from dataclasses import asdict

# Import command types
from ..commands.base import ChatType, DeleteMode, GroupMemberRole, ServerProtocol
from ..command import ChatCommand


class AutoAccept(TypedDict, total=False):
    """Auto accept configuration type."""

    accept_incognito: bool
    auto_reply: Optional[Dict[str, Any]]


def on_off(value: Optional[bool]) -> str:
    """
    Convert boolean to 'on' or 'off' string.

    Args:
        value: Boolean value to convert

    Returns:
        'on' if value is True, 'off' otherwise
    """
    return "on" if value else "off"


def maybe(value: Optional[Any]) -> str:
    """
    Append value with space if it exists, otherwise empty string.

    Args:
        value: Value to append if it exists

    Returns:
        Value with leading space, or empty string if None
    """
    return f" {value}" if value else ""


def maybe_json(value: Optional[Any]) -> str:
    """
    JSON serialize value with prefix if it exists, otherwise empty string.

    Args:
        value: Value to JSON serialize

    Returns:
        JSON string with 'json' prefix and leading space, or empty string if None
    """
    return f" json {json.dumps(value)}" if value else ""


class ChatPagination(TypedDict, total=False):
    """Chat pagination options."""

    count: int
    after: Optional[int]
    before: Optional[int]


def pagination_str(pagination: Union[ChatPagination, Dict[str, Any]]) -> str:
    """
    Format pagination parameters as a string.

    Args:
        pagination: Pagination parameters with count and optionally after/before

    Returns:
        Formatted pagination string for protocol
    """
    base = ""
    if "after" in pagination and pagination["after"] is not None:
        base = f" after={pagination['after']}"
    elif "before" in pagination and pagination["before"] is not None:
        base = f" before={pagination['before']}"

    return f"{base} count={pagination['count']}"


def auto_accept_str(auto_accept: Optional[Union[AutoAccept, Dict[str, Any]]]) -> str:
    """
    Format auto accept settings as a string.

    Args:
        auto_accept: Auto accept configuration with accept_incognito and optional auto_reply

    Returns:
        Formatted auto accept string for protocol
    """
    if not auto_accept:
        return "off"

    msg = auto_accept.get("auto_reply")
    incognito = auto_accept.get("accept_incognito", False)

    result = "on"
    if incognito:
        result += " incognito=on"
    if msg:
        result += f" json {json.dumps(msg)}"

    return result


def cmd_string(cmd: Union[ChatCommand, Dict[str, Any]]) -> str:
    """
    Convert a command object to the protocol string.

    Args:
        cmd: Command object or dictionary with command fields

    Returns:
        String representation of the command for the protocol
    """
    # Convert command object to dictionary if needed
    if hasattr(cmd, "to_dict"):
        cmd_dict = cmd.to_dict()
    elif hasattr(cmd, "__dataclass_fields__"):
        cmd_dict = asdict(cmd)
    else:
        cmd_dict = cmd

    cmd_type = cmd_dict.get("type")

    match cmd_type:
        case "showActiveUser":
            return "/u"

        case "createActiveUser":
            user = {
                "profile": cmd_dict.get("profile"),
                "same_servers": cmd_dict.get("same_servers", False),
                "past_timestamp": cmd_dict.get("past_timestamp", False),
            }
            return f"/_create user {json.dumps(user)}"

        case "listUsers":
            return "/users"

        case "apiSetActiveUser":
            return f"/_user {cmd_dict['user_id']}{maybe_json(cmd_dict.get('view_pwd'))}"

        case "apiHideUser":
            return (
                f"/_hide user {cmd_dict['user_id']} {json.dumps(cmd_dict['view_pwd'])}"
            )

        case "apiUnhideUser":
            return f"/_unhide user {cmd_dict['user_id']} {json.dumps(cmd_dict['view_pwd'])}"

        case "apiMuteUser":
            return f"/_mute user {cmd_dict['user_id']}"

        case "apiUnmuteUser":
            return f"/_unmute user {cmd_dict['user_id']}"

        case "apiDeleteUser":
            return f"/_delete user {cmd_dict['user_id']} del_smp={on_off(cmd_dict.get('del_smp_queues'))}{maybe_json(cmd_dict.get('view_pwd'))}"

        case "startChat":
            return f"/_start subscribe={on_off(cmd_dict.get('subscribe_connections'))} expire={on_off(cmd_dict.get('enable_expire_chat_items'))}"

        case "apiStopChat":
            return "/_stop"

        case "setTempFolder":
            return f"/_temp_folder {cmd_dict['temp_folder_path']}"

        case "setFilesFolder":
            return f"/_files_folder {cmd_dict['files_folder_path']}"

        case "setIncognito":
            return f"/incognito {on_off(cmd_dict['is_incognito'])}"

        case "apiExportArchive":
            return f"/_db export {json.dumps(cmd_dict['config'])}"

        case "apiImportArchive":
            return f"/_db import {json.dumps(cmd_dict['config'])}"

        case "apiDeleteStorage":
            return "/_db delete"

        case "apiGetChats":
            return f"/_get chats pcc={on_off(cmd_dict.get('pending_connections'))}"

        case "apiGetChat":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            pagination = cmd_dict["pagination"]
            pagination_string = (
                pagination_str(pagination) if "count" in pagination else ""
            )

            return (
                f"/_get chat {chat_type_value}{cmd_dict['chat_id']}{pagination_string}"
            )

        case "apiSendMessage":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            chat_id = cmd_dict["chat_id"]
            messages = cmd_dict["messages"]

            # This handles our internal snake_case to wire protocol camelCase conversion
            wire_messages = []
            for msg in messages:
                wire_msg = {}
                # Convert msg_content to msgContent for the wire protocol
                if "msg_content" in msg:
                    wire_msg["msgContent"] = msg["msg_content"]
                elif "msgContent" in msg:  # Handle legacy format during transition
                    wire_msg["msgContent"] = msg["msgContent"]

                # Copy any other fields
                for key, value in msg.items():
                    if key != "msg_content" and key != "msgContent":
                        wire_msg[key] = value

                wire_messages.append(wire_msg)

            return f"/_send {chat_type_value}{chat_id} json {json.dumps(wire_messages)}"

        case "apiUpdateChatItem":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            chat_id = cmd_dict["chat_id"]
            chat_item_id = cmd_dict["chat_item_id"]

            # Get message content with snake_case fallback
            msg_content = None
            if "msg_content" in cmd_dict:
                msg_content = cmd_dict["msg_content"]
            elif "message_content" in cmd_dict:
                msg_content = cmd_dict["message_content"]

            return f"/_update item {chat_type_value}{chat_id} {chat_item_id} json {json.dumps(msg_content)}"

        case "apiDeleteChatItem":
            chat_type = cmd_dict["chat_type"]
            if isinstance(chat_type, ChatType):
                chat_type = chat_type.value

            chat_id = cmd_dict["chat_id"]
            item_id = cmd_dict["chat_item_id"]
            delete_mode = cmd_dict["delete_mode"]
            if isinstance(delete_mode, DeleteMode):
                delete_mode = delete_mode.value

            return f"/_delete item {chat_type}{chat_id} {item_id} {delete_mode}"

        case "apiDeleteMemberChatItem":
            return f"/_delete member item #{cmd_dict['group_id']} {cmd_dict['group_member_id']} {cmd_dict['item_id']}"

        case "apiChatRead":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            item_range = ""
            if "item_range" in cmd_dict and cmd_dict["item_range"]:
                item_range = f" from={cmd_dict['item_range']['from_item']} to={cmd_dict['item_range']['to_item']}"

            return f"/_read chat {chat_type_value}{cmd_dict['chat_id']}{item_range}"

        case "apiDeleteChat":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            return f"/_delete {chat_type_value}{cmd_dict['chat_id']}"

        case "apiClearChat":
            chat_type_value = cmd_dict["chat_type"]
            if isinstance(chat_type_value, ChatType):
                chat_type_value = chat_type_value.value

            return f"/_clear {chat_type_value}{cmd_dict['chat_id']}"

        case "apiAcceptContact":
            return f"/_accept {cmd_dict['contact_req_id']}"

        case "apiRejectContact":
            return f"/_reject {cmd_dict['contact_req_id']}"

        case "apiUpdateProfile":
            return f"/_profile {cmd_dict['user_id']} json {json.dumps(cmd_dict['profile'])}"

        case "apiSetContactAlias":
            return f"/_alias @{cmd_dict['contact_id']} {cmd_dict['local_alias']}"

        case "newGroup":
            return f"/_create group json {json.dumps(format_group_profile(cmd_dict['group_profile']))}"

        case "apiAddMember":
            member_role_value = cmd_dict["member_role"]
            if isinstance(member_role_value, GroupMemberRole):
                member_role_value = member_role_value.value

            return f"/_add #{cmd_dict['group_id']} @{cmd_dict['contact_id']} role={member_role_value}"

        case "apiJoinGroup":
            return f"/_join #{cmd_dict['group_id']}"

        case "apiRemoveMember":
            return f"/_remove #{cmd_dict['group_id']} {cmd_dict['member_id']}"

        case "apiLeaveGroup":
            return f"/_leave #{cmd_dict['group_id']}"

        case "apiListMembers":
            return f"/_members #{cmd_dict['group_id']}"

        case "apiUpdateGroupProfile":
            return f"/_group_profile #{cmd_dict['group_id']} json {json.dumps(format_group_profile(cmd_dict['group_profile']))}"

        case "apiCreateGroupLink":
            member_role_value = cmd_dict["member_role"]
            if isinstance(member_role_value, GroupMemberRole):
                member_role_value = member_role_value.value

            return f"/_create link #{cmd_dict['group_id']} role={member_role_value}"

        case "apiGroupLinkMemberRole":
            member_role_value = cmd_dict["member_role"]
            if isinstance(member_role_value, GroupMemberRole):
                member_role_value = member_role_value.value

            return f"/_set link role #{cmd_dict['group_id']} {member_role_value}"

        case "apiDeleteGroupLink":
            return f"/_delete link #{cmd_dict['group_id']}"

        case "apiGetGroupLink":
            return f"/_get link #{cmd_dict['group_id']}"

        case "apiGetUserProtoServers":
            server_protocol_value = cmd_dict["server_protocol"]
            if isinstance(server_protocol_value, ServerProtocol):
                server_protocol_value = server_protocol_value.value

            return f"/_get servers {cmd_dict['user_id']} {server_protocol_value}"

        case "apiSetUserProtoServers":
            server_protocol_value = cmd_dict["server_protocol"]
            if isinstance(server_protocol_value, ServerProtocol):
                server_protocol_value = server_protocol_value.value

            return f"/_set servers {cmd_dict['user_id']} {server_protocol_value} json {json.dumps(cmd_dict['servers'])}"

        case "apiContactInfo":
            return f"/_info @{cmd_dict['contact_id']}"

        case "apiGroupMemberInfo":
            return f"/_info #{cmd_dict['group_id']} {cmd_dict['member_id']}"

        case "apiGetContactCode":
            return f"/_verify @{cmd_dict['contact_id']}"

        case "apiGetGroupMemberCode":
            return f"/_verify #{cmd_dict['group_id']} {cmd_dict['group_member_id']}"

        case "apiVerifyContact":
            return f"/_verify @{cmd_dict['contact_id']} {cmd_dict['connection_code']}"

        case "apiVerifyGroupMember":
            return f"/_verify #{cmd_dict['group_id']} {cmd_dict['group_member_id']} {cmd_dict['connection_code']}"

        case "addContact":
            return "/contacts"

        case "connect":
            return f"/c {cmd_dict['conn_req']}"

        case "connectSimplex":
            return "/c"

        case "createMyAddress":
            return "/create_address"

        case "deleteMyAddress":
            return "/delete_address"

        case "showMyAddress":
            return "/show_address"

        case "setProfileAddress":
            return f"/profile_address {on_off(cmd_dict['include_in_profile'])}"

        case "addressAutoAccept":
            auto_accept_dict = cmd_dict.get("auto_accept")
            return f"/auto_accept {auto_accept_str(auto_accept_dict)}"

        case "apiCreateMyAddress":
            return f"/_create address {cmd_dict['user_id']}"

        case "apiDeleteMyAddress":
            return f"/_delete address {cmd_dict['user_id']}"

        case "apiShowMyAddress":
            return f"/_get address {cmd_dict['user_id']}"

        case "apiSetProfileAddress":
            return f"/_set profile_address {cmd_dict['user_id']} {on_off(cmd_dict['include_in_profile'])}"

        case "apiAddressAutoAccept":
            auto_accept_dict = cmd_dict.get("auto_accept")
            return f"/_set auto_accept {cmd_dict['user_id']} {auto_accept_str(auto_accept_dict)}"

        case "receiveFile":
            return f"/rf {cmd_dict['file_id']}{maybe(cmd_dict.get('file_path'))}"

        case "cancelFile":
            return f"/cf {cmd_dict['file_id']}"

        case "fileStatus":
            return f"/fs {cmd_dict['file_id']}"

        case _:
            # For other commands, convert to JSON string
            return json.dumps(cmd_dict)


def format_group_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a group profile from snake_case (Python) to camelCase (wire protocol).

    Args:
        profile: Group profile with snake_case keys

    Returns:
        Group profile with camelCase keys for the wire protocol
    """
    wire_profile = {}

    # Map snake_case to camelCase
    key_mapping = {
        "display_name": "displayName",
        "full_name": "fullName",
        "description": "description",  # No change needed
        "image": "image",  # No change needed
    }

    for key, value in profile.items():
        wire_key = key_mapping.get(key, key)
        wire_profile[wire_key] = value

    return wire_profile
