"""
Tests for enums and example command dataclasses in simplexbot.command
"""

from simplexbot.command import (
    AddressAutoAccept,
    APIAcceptContact,
    APIAddMember,
    APIChatRead,
    APIClearChat,
    APICreateGroupLink,
    APIDeleteChat,
    APIDeleteChatItem,
    APIDeleteGroupLink,
    APIDeleteMemberChatItem,
    APIDeleteStorage,
    APIDeleteUser,
    APIExportArchive,
    APIGetChat,
    APIGetChats,
    APIGetGroupLink,
    APIGroupLinkMemberRole,
    APIHideUser,
    APIImportArchive,
    APIJoinGroup,
    APILeaveGroup,
    APIListMembers,
    APIMuteUser,
    APIRejectContact,
    APIRemoveMember,
    APISendMessage,
    APISetActiveUser,
    APISetContactAlias,
    APIUnhideUser,
    APIUnmuteUser,
    APIUpdateChatItem,
    APIUpdateGroupProfile,
    APIUpdateProfile,
    APIVerifyContact,
    APIVerifyGroupMember,
    ArchiveConfig,
    CancelFile,
    ChatPagination,
    ChatType,
    ComposedMessage,
    CreateActiveUser,
    CreateMyAddress,
    DeleteMode,
    DeleteMyAddress,
    FileStatus,
    GroupMemberRole,
    GroupProfile,
    ListUsers,
    MsgContent,
    NewGroup,
    Profile,
    ReceiveFile,
    SetFilesFolder,
    SetIncognito,
    SetProfileAddress,
    SetTempFolder,
    ShowActiveUser,
    ShowMyAddress,
    StartChat,
)


def test_enum_values():
    assert ChatType.DIRECT.value == "@"
    assert ChatType.GROUP.value == "#"
    assert ChatType.CONTACT_REQUEST.value == "<@"
    assert DeleteMode.BROADCAST.value == "broadcast"
    assert DeleteMode.INTERNAL.value == "internal"
    assert GroupMemberRole.MEMBER.value == "member"
    assert GroupMemberRole.ADMIN.value == "admin"
    assert GroupMemberRole.OWNER.value == "owner"


def test_show_active_user_dataclass():
    cmd = ShowActiveUser()
    assert cmd.type == "showActiveUser"


def test_create_active_user_defaults():
    cmd = CreateActiveUser()
    assert cmd.type == "createActiveUser"
    assert cmd.profile is None
    assert cmd.same_servers is True
    assert cmd.past_timestamp is False


def test_create_active_user_with_profile():
    profile = Profile(
        display_name="Alice", full_name="Alice Smith", image=None, contact_link=None
    )
    cmd = CreateActiveUser(profile=profile, same_servers=False, past_timestamp=True)
    assert cmd.profile.display_name == "Alice"
    assert not cmd.same_servers
    assert cmd.past_timestamp


def test_list_users_dataclass():
    cmd = ListUsers()
    assert cmd.type == "listUsers"


def test_api_set_active_user_required():
    cmd = APISetActiveUser(user_id=42)
    assert cmd.type == "apiSetActiveUser"
    assert cmd.user_id == 42
    assert cmd.view_pwd is None
    cmd2 = APISetActiveUser(user_id=1, view_pwd="pw")
    assert cmd2.view_pwd == "pw"


def test_api_hide_unhide_user():
    hide = APIHideUser(user_id=5, view_pwd="pw")
    assert hide.type == "apiHideUser"
    assert hide.user_id == 5
    assert hide.view_pwd == "pw"
    unhide = APIUnhideUser(user_id=5, view_pwd="pw")
    assert unhide.type == "apiUnhideUser"
    assert unhide.user_id == 5
    assert unhide.view_pwd == "pw"


def test_api_mute_unmute_user():
    mute = APIMuteUser(user_id=7)
    assert mute.type == "apiMuteUser"
    assert mute.user_id == 7
    unmute = APIUnmuteUser(user_id=7)
    assert unmute.type == "apiUnmuteUser"
    assert unmute.user_id == 7


def test_api_delete_user():
    delete = APIDeleteUser(user_id=99, del_smp_queues=True)
    assert delete.type == "apiDeleteUser"
    assert delete.user_id == 99
    assert delete.del_smp_queues is True
    assert delete.view_pwd is None
    delete2 = APIDeleteUser(user_id=1, del_smp_queues=False, view_pwd="pw")
    assert delete2.view_pwd == "pw"


def test_start_chat_defaults():
    cmd = StartChat()
    assert cmd.type == "startChat"
    assert cmd.subscribe_connections is None
    assert cmd.enable_expire_chat_items is None
    assert cmd.start_xftp_workers is None


def test_set_temp_and_files_folder():
    temp = SetTempFolder(temp_folder="/tmp")
    files = SetFilesFolder(file_path="/files")
    assert temp.type == "setTempFolder"
    assert temp.temp_folder == "/tmp"
    assert files.type == "setFilesFolder"
    assert files.file_path == "/files"


def test_set_incognito():
    cmd = SetIncognito(incognito=True)
    assert cmd.type == "setIncognito"
    assert cmd.incognito is True


def test_archive_config_and_export_import():
    cfg = ArchiveConfig(archive_path="/archive.zip")
    export = APIExportArchive(config=cfg)
    imp = APIImportArchive(config=cfg)
    assert export.type == "apiExportArchive"
    assert export.config.archive_path == "/archive.zip"
    assert imp.type == "apiImportArchive"
    assert imp.config == cfg


def test_api_delete_storage():
    cmd = APIDeleteStorage()
    assert cmd.type == "apiDeleteStorage"


def test_chat_pagination():
    pag = ChatPagination(count=10, after=1, before=5)
    assert pag.count == 10
    assert pag.after == 1
    assert pag.before == 5


def test_api_get_chats_and_chat():
    pag = ChatPagination(count=5)
    get_chats = APIGetChats(user_id=2)
    get_chat = APIGetChat(chat_type=ChatType.DIRECT, chat_id=3, pagination=pag)
    assert get_chats.type == "apiGetChats"
    assert get_chats.user_id == 2
    assert get_chat.type == "apiGetChat"
    assert get_chat.chat_type == ChatType.DIRECT
    assert get_chat.pagination == pag


def test_msg_content_and_composed_message():
    from simplexbot.models.message import MCText, ComposedMessage
    mc = MCText(text="hello")
    cm = ComposedMessage(msg_content=mc, file_path="/file.txt", quoted_item_id=5)
    assert cm.msg_content.type == "text"
    assert cm.file_path == "/file.txt"
    assert cm.quoted_item_id == 5


def test_api_send_message_and_update_chat_item():
    from simplexbot.models.message import MCText
    mc = MCText(text="hi")
    from simplexbot.models.message import ComposedMessage
    cm = ComposedMessage(msg_content=mc)
    send = APISendMessage(chat_type=ChatType.DIRECT, chat_id=1, messages=[cm])
    update = APIUpdateChatItem(
        chat_type=ChatType.DIRECT, chat_id=1, chat_item_id=2, msg_content=mc
    )
    assert send.type == "apiSendMessage"
    assert update.type == "apiUpdateChatItem"
    assert update.chat_item_id == 2


def test_api_delete_chat_item_and_member_chat_item():
    del_item = APIDeleteChatItem(
        chat_type=ChatType.DIRECT,
        chat_id=1,
        chat_item_id=2,
        delete_mode=DeleteMode.BROADCAST,
    )
    del_member = APIDeleteMemberChatItem(group_id=1, group_member_id=2, item_id=3)
    assert del_item.type == "apiDeleteChatItem"
    assert del_item.delete_mode == DeleteMode.BROADCAST
    assert del_member.type == "apiDeleteMemberChatItem"
    assert del_member.group_id == 1


def test_api_chat_read_delete_clear():
    read = APIChatRead(chat_type=ChatType.DIRECT, chat_id=1, item_range=(1, 2))
    delete = APIDeleteChat(chat_type=ChatType.DIRECT, chat_id=1)
    clear = APIClearChat(chat_type=ChatType.DIRECT, chat_id=1)
    assert read.type == "apiChatRead"
    assert read.item_range == (1, 2)
    assert delete.type == "apiDeleteChat"
    assert clear.type == "apiClearChat"


def test_api_accept_and_reject_contact():
    accept = APIAcceptContact(contact_req_id=1)
    reject = APIRejectContact(contact_req_id=2)
    assert accept.type == "apiAcceptContact"
    assert accept.contact_req_id == 1
    assert reject.type == "apiRejectContact"
    assert reject.contact_req_id == 2


def test_api_update_profile_and_set_alias():
    profile = Profile(display_name="Bob", full_name="Bob Smith")
    update = APIUpdateProfile(user_id=1, profile=profile)
    alias = APISetContactAlias(contact_id=5, local_alias="Bobby")
    assert update.type == "apiUpdateProfile"
    assert update.profile.display_name == "Bob"
    assert alias.type == "apiSetContactAlias"
    assert alias.local_alias == "Bobby"


def test_group_profile_and_new_group():
    gp = GroupProfile(display_name="Dev", full_name="Developers")
    new_group = NewGroup(group_profile=gp)
    assert gp.display_name == "Dev"
    assert new_group.type == "newGroup"
    assert new_group.group_profile.full_name == "Developers"


def test_api_add_join_remove_leave_list_update_group():
    gp = GroupProfile(display_name="QA", full_name="QA Team")
    add = APIAddMember(group_id=1, contact_id=2, member_role=GroupMemberRole.MEMBER)
    join = APIJoinGroup(group_id=1)
    remove = APIRemoveMember(group_id=1, member_id=2)
    leave = APILeaveGroup(group_id=1)
    list_members = APIListMembers(group_id=1)
    update = APIUpdateGroupProfile(group_id=1, group_profile=gp)
    assert add.type == "apiAddMember"
    assert join.type == "apiJoinGroup"
    assert remove.type == "apiRemoveMember"
    assert leave.type == "apiLeaveGroup"
    assert list_members.type == "apiListMembers"
    assert update.type == "apiUpdateGroupProfile"
    assert update.group_profile.display_name == "QA"


def test_api_group_links():
    create = APICreateGroupLink(group_id=1, member_role=GroupMemberRole.ADMIN)
    role = APIGroupLinkMemberRole(group_id=1, member_role=GroupMemberRole.OWNER)
    delete = APIDeleteGroupLink(group_id=1)
    get = APIGetGroupLink(group_id=1)
    assert create.type == "apiCreateGroupLink"
    assert role.member_role == GroupMemberRole.OWNER
    assert delete.type == "apiDeleteGroupLink"
    assert get.type == "apiGetGroupLink"


def test_address_and_profile_commands():
    create = CreateMyAddress()
    delete = DeleteMyAddress()
    show = ShowMyAddress()
    set_profile = SetProfileAddress(include_in_profile=True)
    auto = AddressAutoAccept(auto_accept=True)
    assert create.type == "createMyAddress"
    assert delete.type == "deleteMyAddress"
    assert show.type == "showMyAddress"
    assert set_profile.include_in_profile is True
    assert auto.auto_accept is True


def test_receive_cancel_file_status():
    receive = ReceiveFile(file_id=1, file_path="/f")
    cancel = CancelFile(file_id=2)
    status = FileStatus(file_id=3)
    assert receive.type == "receiveFile"
    assert receive.file_path == "/f"
    assert cancel.type == "cancelFile"
    assert status.type == "fileStatus"
    assert status.file_id == 3


def test_api_verify_contact_and_group_member():
    verify_contact = APIVerifyContact(contact_id=1, connection_code="abc")
    verify_group = APIVerifyGroupMember(
        group_id=2, group_member_id=3, connection_code="xyz"
    )
    assert verify_contact.type == "apiVerifyContact"
    assert verify_contact.connection_code == "abc"
    assert verify_group.type == "apiVerifyGroupMember"
    assert verify_group.group_member_id == 3
    assert verify_group.connection_code == "xyz"
