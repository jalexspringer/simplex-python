"""
Tests for simplexbot.response dataclasses.

Covers construction, field values, and typing for initial response types.
"""

from simplexbot.command import Profile
from simplexbot.response import (
    CRActiveUser,
    CRApiChats,
    CRChatItemDeleted,
    CRChatItemStatusUpdated,
    CRChatItemUpdated,
    CRChatRunning,
    CRChatStarted,
    CRChatStopped,
    CRCmdOk,
    CRMsgIntegrityError,
    CRNewChatItems,
    CRUsersList,
)


def make_profile(display_name: str) -> Profile:
    return Profile(display_name=display_name, full_name=f"{display_name} Smith")


def test_cr_active_user():
    profile = make_profile("Alice")
    resp = CRActiveUser(user=profile)
    assert resp.type == "activeUser"
    assert resp.user.display_name == "Alice"


def test_cr_users_list():
    profiles = [make_profile("Alice"), make_profile("Bob")]
    resp = CRUsersList(users=profiles)
    assert resp.type == "usersList"
    assert len(resp.users) == 2
    assert resp.users[1].display_name == "Bob"


def test_cr_chat_started():
    resp = CRChatStarted()
    assert resp.type == "chatStarted"


def test_cr_chat_running():
    resp = CRChatRunning()
    assert resp.type == "chatRunning"


def test_cr_chat_stopped():
    resp = CRChatStopped()
    assert resp.type == "chatStopped"


def test_cr_api_chats():
    profile = make_profile("Charlie")
    resp = CRApiChats(user=profile, chats=[{"id": 1}, {"id": 2}])
    assert resp.type == "apiChats"
    assert resp.user.display_name == "Charlie"
    assert isinstance(resp.chats, list)
    assert resp.chats[0]["id"] == 1


def test_cr_new_chat_items():
    profile = make_profile("Dana")
    chat_items = [{"id": 123}, {"id": 456}]
    resp = CRNewChatItems(user=profile, chat_items=chat_items)
    assert resp.type == "newChatItems"
    assert resp.user.display_name == "Dana"
    assert isinstance(resp.chat_items, list)
    assert resp.chat_items[1]["id"] == 456


def test_cr_chat_item_status_updated():
    profile = make_profile("Eve")
    chat_item = {"id": 789, "status": "read"}
    resp = CRChatItemStatusUpdated(user=profile, chat_item=chat_item)
    assert resp.type == "chatItemStatusUpdated"
    assert resp.user.display_name == "Eve"
    assert resp.chat_item["status"] == "read"


def test_cr_chat_item_updated():
    profile = make_profile("Frank")
    chat_item = {"id": 111, "content": "hello"}
    resp = CRChatItemUpdated(user=profile, chat_item=chat_item)
    assert resp.type == "chatItemUpdated"
    assert resp.user.display_name == "Frank"
    assert resp.chat_item["content"] == "hello"


def test_cr_chat_item_deleted():
    profile = make_profile("Grace")
    deleted = {"id": 222}
    to_item = {"id": 333}
    resp = CRChatItemDeleted(
        user=profile, deleted_chat_item=deleted, to_chat_item=to_item, by_user=True
    )
    assert resp.type == "chatItemDeleted"
    assert resp.user.display_name == "Grace"
    assert resp.deleted_chat_item["id"] == 222
    assert resp.to_chat_item["id"] == 333
    assert resp.by_user is True


def test_cr_msg_integrity_error():
    profile = make_profile("Heidi")
    msg_error = {"type": "checksum", "details": "corrupt"}
    resp = CRMsgIntegrityError(user=profile, msg_error=msg_error)
    assert resp.type == "msgIntegrityError"
    assert resp.user.display_name == "Heidi"
    assert resp.msg_error["type"] == "checksum"


def test_cr_cmd_ok():
    profile = make_profile("Ivan")
    resp = CRCmdOk(user_=profile)
    assert resp.type == "cmdOk"
    assert resp.user_.display_name == "Ivan"
