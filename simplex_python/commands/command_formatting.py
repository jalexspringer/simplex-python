"""
Command formatting utilities for Simplex protocol.

"""

import json
from typing import Any, Dict, Optional

from .base import BaseCommand, ServerProtocol


def cmd_string(cmd: BaseCommand) -> str:
    """Convert a command object to its string representation for the SimpleX Chat protocol.

    This function translates BaseCommand objects into the string format used in the
    SimpleX Chat WebSocket API, following the same pattern as the Haskell implementation
    in Simplex.Chat.Controller.

    The command translation relies on the 'type' attribute of each command class,
    which must be defined for all BaseCommand subclasses. This maps directly to the
    ChatCommand data type in the Haskell codebase.

    Args:
        cmd: A BaseCommand instance with a defined 'type' attribute.
             The 'type' value determines which protocol command will be generated.

    Returns:
        str: The string representation of the command formatted according to
             the SimpleX Chat protocol requirements. For example:
             - "showActiveUser" returns "/u"
             - "createActiveUser" returns a JSON payload with user profile data

    Raises:
        ValueError: If the command type is not recognized or supported.
        AttributeError: If the cmd object doesn't have a 'type' attribute.
    """
    match cmd.type:
        case "showActiveUser":
            return "/u"
        case "createActiveUser":
            user = {
                "profile": cmd.profile,
                "sameServers": cmd.sameServers,
                "pastTimestamp": cmd.pastTimestamp,
            }
            return f"/_create user {json.dumps(user)}"
        case "listUsers":
            return "/users"
        case "apiSetActiveUser":
            view_pwd = maybe_json(cmd.viewPwd)
            return f"/_user {cmd.userId}{view_pwd}"
        case "apiHideUser":
            return f"/_hide user {cmd.userId} {json.dumps(cmd.viewPwd)}"
        case "apiUnhideUser":
            return f"/_unhide user {cmd.userId} {json.dumps(cmd.viewPwd)}"
        case "apiMuteUser":
            return f"/_mute user {cmd.userId}"
        case "apiUnmuteUser":
            return f"/_unmute user {cmd.userId}"
        case "apiDeleteUser":
            view_pwd = maybe_json(cmd.viewPwd)
            return f"/_delete user {cmd.userId} del_smp={on_off(cmd.delSMPQueues)}{view_pwd}"
        case "startChat":
            subscribe = "on" if cmd.subscribeConnections else "off"
            expire = "on" if cmd.enableExpireChatItems else "off"
            return f"/_start subscribe={subscribe} expire={expire}"
        case "apiStopChat":
            return "/_stop"
        case "setTempFolder":
            return f"/_temp_folder {cmd.tempFolder}"
        case "setFilesFolder":
            return f"/_files_folder {cmd.filePath}"
        case "setIncognito":
            return f"/incognito {on_off(cmd.incognito)}"
        case "apiExportArchive":
            return f"/_db export {json.dumps(cmd.config)}"
        case "apiImportArchive":
            return f"/_db import {json.dumps(cmd.config)}"
        case "apiDeleteStorage":
            return "/_db delete"
        case "apiGetChats":
            return "/chats"
        case "apiGetChat":
            pagination = pagination_str(cmd.pagination)
            return f"/_get chat {cmd.chatType}{cmd.chatId}{pagination}"
        case "apiSendMessage":
            return f"/_send {cmd.chatType}{cmd.chatId} json {json.dumps(cmd.messages)}"
        case "apiUpdateChatItem":
            return f"/_update item {cmd.chatType}{cmd.chatId} {cmd.chatItemId} json {json.dumps(cmd.msgContent)}"
        case "apiDeleteChatItem":
            return f"/_delete item {cmd.chatType}{cmd.chatId} {cmd.chatItemId} {cmd.deleteMode}"
        case "apiDeleteMemberChatItem":
            return (
                f"/_delete member item #{cmd.groupId} {cmd.groupMemberId} {cmd.itemId}"
            )
        case "apiChatRead":
            item_range = ""
            if getattr(cmd, "itemRange", None):
                item_range = (
                    f" from={cmd.itemRange['fromItem']} to={cmd.itemRange['toItem']}"
                )
            return f"/_read chat {cmd.chatType}{cmd.chatId}{item_range}"
        case "apiDeleteChat":
            return f"/_delete {cmd.chatType}{cmd.chatId}"
        case "apiClearChat":
            return f"/_clear chat {cmd.chatType}{cmd.chatId}"
        case "apiAcceptContact":
            return f"/_accept {cmd.contactReqId}"
        case "apiRejectContact":
            return f"/_reject {cmd.contactReqId}"
        case "apiUpdateProfile":
            return f"/_profile {cmd.userId} {json.dumps(cmd.profile)}"
        case "apiSetContactAlias":
            return f"/_set alias @{cmd.contactId} {cmd.localAlias.strip()}"
        case "newGroup":
            return f"/group {cmd.groupProfile['displayName']} {cmd.groupProfile['fullName']} {cmd.groupProfile['image']}"
        case "apiAddMember":
            return f"/_add #{cmd.groupId} {cmd.contactId} {cmd.memberRole}"
        case "apiJoinGroup":
            return f"/_join #{cmd.groupId}"
        case "apiRemoveMember":
            return f"/_remove #{cmd.groupId} {cmd.memberId}"
        case "apiLeaveGroup":
            return f"/_leave #{cmd.groupId}"
        case "apiListMembers":
            return f"/_members #{cmd.groupId}"
        case "apiUpdateGroupProfile":
            return f"/_group_profile #{cmd.groupId} {json.dumps(cmd.groupProfile)}"
        case "apiCreateGroupLink":
            return f"/_create link #{cmd.groupId} {cmd.memberRole}"
        case "apiGroupLinkMemberRole":
            return f"/_set link role #{cmd.groupId} {cmd.memberRole}"
        case "apiDeleteGroupLink":
            return f"/_delete link #{cmd.groupId}"
        case "apiGetGroupLink":
            return f"/_get link #{cmd.groupId}"
        case "apiGetUserProtoServers":
            if cmd.serverProtocol == ServerProtocol.SMP:
                return "/smp"
            if cmd.serverProtocol == ServerProtocol.XFTP:
                return "/xftp"
        case "apiSetUserProtoServers":
            return f"/_servers {cmd.userId} {cmd.serverProtocol} {json.dumps({'servers': cmd.servers})}"
        case "apiContactInfo":
            return f"/_info @{cmd.contactId}"
        case "apiGroupMemberInfo":
            return f"/_info #{cmd.groupId} {cmd.memberId}"
        case "apiGetContactCode":
            return f"/_get code @{cmd.contactId}"
        case "apiGetGroupMemberCode":
            return f"/_get code #{cmd.groupId} {cmd.groupMemberId}"
        case "apiVerifyContact":
            conn_code = maybe(cmd.connectionCode)
            return f"/_verify code @{cmd.contactId}{conn_code}"
        case "apiVerifyGroupMember":
            conn_code = maybe(cmd.connectionCode)
            return f"/_verify code #{cmd.groupId} {cmd.groupMemberId}{conn_code}"
        case "addContact":
            return "/connect"
        case "connect":
            return f"/connect {cmd.connReq}"
        case "connectSimplex":
            return "/simplex"
        case "createMyAddress":
            return "/address"
        case "deleteMyAddress":
            return "/delete_address"
        case "showMyAddress":
            return "/show_address"
        case "setProfileAddress":
            return f"/profile_address {on_off(cmd.includeInProfile)}"
        case "addressAutoAccept":
            return f"/auto_accept {auto_accept_str(cmd.autoAccept)}"
        case "apiCreateMyAddress":
            return f"/_address {cmd.userId}"
        case "apiDeleteMyAddress":
            return f"/_delete_address {cmd.userId}"
        case "apiShowMyAddress":
            return f"/_show_address {cmd.userId}"
        case "apiSetProfileAddress":
            return f"/_profile_address {cmd.userId} {on_off(cmd.includeInProfile)}"
        case "apiAddressAutoAccept":
            return f"/_auto_accept {cmd.userId} {auto_accept_str(cmd.autoAccept)}"
        case "receiveFile":
            file_path = f" {cmd.filePath}" if getattr(cmd, "filePath", None) else ""
            return f"/freceive {cmd.fileId}{file_path}"
        case "cancelFile":
            return f"/fcancel {cmd.fileId}"
        case "fileStatus":
            return f"/fstatus {cmd.fileId}"


def pagination_str(cp: Optional[Dict[str, Any]]) -> str:
    if not cp:
        return ""

    base = ""
    if "after" in cp:
        base = f" after={cp['after']}"
    elif "before" in cp:
        base = f" before={cp['before']}"

    return f"{base} count={cp['count']}"


def maybe(value: Optional[Any]) -> str:
    return f" {value}" if value is not None else ""


def maybe_json(value: Optional[Any]) -> str:
    return f" json {json.dumps(value)}" if value is not None else ""


def on_off(value: Optional[Any]) -> str:
    return "on" if value else "off"


def auto_accept_str(auto_accept: Optional[Dict[str, Any]]) -> str:
    if not auto_accept:
        return "off"

    msg = auto_accept.get("autoReply")
    incognito_part = " incognito=on" if auto_accept.get("acceptIncognito") else ""
    msg_part = f" json {json.dumps(msg)}" if msg else ""

    return f"on{incognito_part}{msg_part}"
