"""
Utilities for Simplex Python client.

Includes protocol command stringification for parity with the TypeScript client.
"""

from typing import Any, Dict, Optional
import json
from dataclasses import asdict

# Import all command types
from .command import ChatCommand
from .commands.base import ChatType, DeleteMode, GroupMemberRole, ServerProtocol
from .models.pagination import ChatPagination
from .models.archive import AutoAccept


def on_off(value: Optional[bool]) -> str:
    """Convert boolean to 'on' or 'off' string."""
    return "on" if value else "off"


def maybe(value: Optional[Any]) -> str:
    """Append value with space if it exists, otherwise empty string."""
    return f" {value}" if value else ""


def maybe_json(value: Optional[Any]) -> str:
    """JSON serialize value with prefix if it exists, otherwise empty string."""
    return f" json {json.dumps(value)}" if value else ""


def pagination_str(pagination: ChatPagination) -> str:
    """Format pagination parameters as a string."""
    base = ""
    if pagination.after is not None:
        base = f" after={pagination.after}"
    elif pagination.before is not None:
        base = f" before={pagination.before}"
    return f"{base} count={pagination.count}"


def auto_accept_str(auto_accept: Optional[Dict[str, Any]]) -> str:
    """Format auto accept settings as a string."""
    if not auto_accept:
        return "off"
    msg = auto_accept.get("auto_reply")
    incognito = auto_accept.get("accept_incognito", False)
    return (
        "on"
        + (" incognito=on" if incognito else "")
        + (f" json {json.dumps(msg)}" if msg else "")
    )


def cmd_string(cmd: ChatCommand) -> str:
    """
    Convert a command object to the protocol string.
    Mirrors the TypeScript cmdString function.

    Args:
        cmd: Any command dataclass

    Returns:
        String representation of the command for the protocol
    """
    cmd_dict = asdict(cmd)
    cmd_type = cmd_dict.get("type")

    match cmd_type:
        case "showActiveUser":
            return "/u"

        case "createActiveUser":
            user = {
                "profile": cmd_dict.get("profile"),
                "sameServers": cmd_dict.get("same_servers"),
                "pastTimestamp": cmd_dict.get("past_timestamp"),
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
            return f"/_temp_folder {cmd_dict['temp_folder']}"

        case "setFilesFolder":
            return f"/_files_folder {cmd_dict['file_path']}"

        case "setIncognito":
            return f"/incognito {on_off(cmd_dict['incognito'])}"

        case "apiExportArchive":
            return f"/_db export {json.dumps(cmd_dict['config'])}"

        case "apiImportArchive":
            return f"/_db import {json.dumps(cmd_dict['config'])}"

        case "apiDeleteStorage":
            return "/_db delete"

        case "apiGetChats":
            return f"/_get chats pcc={on_off(cmd_dict.get('pending_connections'))}"

        case "apiGetChat":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            pagination = cmd_dict["pagination"]
            pagination_string = (
                pagination_str(pagination) if hasattr(pagination, "count") else ""
            )
            return (
                f"/_get chat {chat_type_value}{cmd_dict['chat_id']}{pagination_string}"
            )

        case "apiSendMessage":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            return f"/_send {chat_type_value}{cmd_dict['chat_id']} json {json.dumps(cmd_dict['messages'])}"

        case "apiUpdateChatItem":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            return f"/_update item {chat_type_value}{cmd_dict['chat_id']} {cmd_dict['chat_item_id']} json {json.dumps(cmd_dict['msg_content'])}"

        case "apiDeleteChatItem":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            delete_mode_value = (
                cmd_dict["delete_mode"].value
                if isinstance(cmd_dict["delete_mode"], DeleteMode)
                else cmd_dict["delete_mode"]
            )
            return f"/_delete item {chat_type_value}{cmd_dict['chat_id']} {cmd_dict['chat_item_id']} {delete_mode_value}"

        case "apiDeleteMemberChatItem":
            return f"/_delete member item #{cmd_dict['group_id']} {cmd_dict['group_member_id']} {cmd_dict['item_id']}"

        case "apiChatRead":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            item_range = ""
            if cmd_dict.get("item_range"):
                item_range = f" from={cmd_dict['item_range']['from_item']} to={cmd_dict['item_range']['to_item']}"
            return f"/_read chat {chat_type_value}{cmd_dict['chat_id']}{item_range}"

        case "apiDeleteChat":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            return f"/_delete {chat_type_value}{cmd_dict['chat_id']}"

        case "apiClearChat":
            chat_type_value = (
                cmd_dict["chat_type"].value
                if isinstance(cmd_dict["chat_type"], ChatType)
                else cmd_dict["chat_type"]
            )
            return f"/_clear chat {chat_type_value}{cmd_dict['chat_id']}"

        case "apiAcceptContact":
            return f"/_accept {cmd_dict['contact_req_id']}"

        case "apiRejectContact":
            return f"/_reject {cmd_dict['contact_req_id']}"

        case "apiUpdateProfile":
            return f"/_profile {cmd_dict['user_id']} {json.dumps(cmd_dict['profile'])}"

        case "apiSetContactAlias":
            return f"/_set alias @{cmd_dict['contact_id']} {cmd_dict['local_alias'].strip()}"

        case "newGroup":
            return f"/_group {json.dumps(cmd_dict['group_profile'])}"

        case "apiAddMember":
            member_role_value = (
                cmd_dict["member_role"].value
                if isinstance(cmd_dict["member_role"], GroupMemberRole)
                else cmd_dict["member_role"]
            )
            return f"/_add #{cmd_dict['group_id']} {cmd_dict['contact_id']} {member_role_value}"

        case "apiJoinGroup":
            return f"/_join #{cmd_dict['group_id']}"

        case "apiRemoveMember":
            return f"/_remove #{cmd_dict['group_id']} {cmd_dict['member_id']}"

        case "apiLeaveGroup":
            return f"/_leave #{cmd_dict['group_id']}"

        case "apiListMembers":
            return f"/_members #{cmd_dict['group_id']}"

        case "apiUpdateGroupProfile":
            return f"/_group_profile #{cmd_dict['group_id']} {json.dumps(cmd_dict['group_profile'])}"

        case "apiCreateGroupLink":
            member_role_value = (
                cmd_dict["member_role"].value
                if isinstance(cmd_dict["member_role"], GroupMemberRole)
                else cmd_dict["member_role"]
            )
            return f"/_create link #{cmd_dict['group_id']} {member_role_value}"

        case "apiGroupLinkMemberRole":
            member_role_value = (
                cmd_dict["member_role"].value
                if isinstance(cmd_dict["member_role"], GroupMemberRole)
                else cmd_dict["member_role"]
            )
            return f"/_set link role #{cmd_dict['group_id']} {member_role_value}"

        case "apiDeleteGroupLink":
            return f"/_delete link #{cmd_dict['group_id']}"

        case "apiGetGroupLink":
            return f"/_get link #{cmd_dict['group_id']}"

        case "apiVerifyContact":
            return f"/_verify code @{cmd_dict['contact_id']}{maybe(cmd_dict.get('connection_code'))}"

        case "apiVerifyGroupMember":
            return f"/_verify code #{cmd_dict['group_id']} {cmd_dict['group_member_id']}{maybe(cmd_dict.get('connection_code'))}"

        case "apiGetUserProtoServers":
            protocol_value = (
                cmd_dict["server_protocol"].value
                if isinstance(cmd_dict["server_protocol"], ServerProtocol)
                else cmd_dict["server_protocol"]
            )
            return f"/_servers {cmd_dict['user_id']} {protocol_value}"

        case "apiSetUserProtoServers":
            protocol_value = (
                cmd_dict["server_protocol"].value
                if isinstance(cmd_dict["server_protocol"], ServerProtocol)
                else cmd_dict["server_protocol"]
            )
            return f"/_servers {cmd_dict['user_id']} {protocol_value} {json.dumps({'servers': cmd_dict['servers']})}"

        case "apiContactInfo":
            return f"/_info @{cmd_dict['contact_id']}"

        case "apiGroupMemberInfo":
            return f"/_info #{cmd_dict['group_id']} {cmd_dict['member_id']}"

        case "apiGetContactCode":
            return f"/_get code @{cmd_dict['contact_id']}"

        case "apiGetGroupMemberCode":
            return f"/_get code #{cmd_dict['group_id']} {cmd_dict['group_member_id']}"

        case "addContact":
            return "/connect"

        case "connect":
            return f"/connect {cmd_dict['conn_req']}"

        case "connectSimplex":
            return "/simplex"

        case "createMyAddress":
            return "/address"

        case "deleteMyAddress":
            return "/delete_address"

        case "showMyAddress":
            return "/show_address"

        case "setProfileAddress":
            return f"/profile_address {on_off(cmd_dict['include_in_profile'])}"

        case "addressAutoAccept":
            # Accepts dict or object for auto_accept; handle both
            auto_accept = cmd_dict.get("auto_accept")
            if isinstance(auto_accept, dict):
                return f"/auto_accept {auto_accept_str(auto_accept)}"
            elif auto_accept:
                return f"/auto_accept {auto_accept_str(asdict(auto_accept))}"
            return "/auto_accept off"

        case "apiCreateMyAddress":
            return f"/_address {cmd_dict['user_id']}"

        case "apiDeleteMyAddress":
            return f"/_delete_address {cmd_dict['user_id']}"

        case "apiShowMyAddress":
            return f"/_show_address {cmd_dict['user_id']}"

        case "apiSetProfileAddress":
            return f"/_profile_address {cmd_dict['user_id']} {on_off(cmd_dict['include_in_profile'])}"

        case "apiAddressAutoAccept":
            # Accepts dict or object for auto_accept; handle both
            auto_accept = cmd_dict.get("auto_accept")
            if isinstance(auto_accept, dict):
                return f"/_auto_accept {cmd_dict['user_id']} {auto_accept_str(auto_accept)}"
            elif auto_accept:
                return f"/_auto_accept {cmd_dict['user_id']} {auto_accept_str(asdict(auto_accept))}"
            return f"/_auto_accept {cmd_dict['user_id']} off"

        case "receiveFile":
            file_path = cmd_dict.get("file_path", "")
            return (
                f"/freceive {cmd_dict['file_id']}{' ' + file_path if file_path else ''}"
            )

        case "cancelFile":
            return f"/fcancel {cmd_dict['file_id']}"

        case "fileStatus":
            return f"/fstatus {cmd_dict['file_id']}"

        case _:
            raise ValueError(f"Unknown or unimplemented command type: {cmd_type}")
