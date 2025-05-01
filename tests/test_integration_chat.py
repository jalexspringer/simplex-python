import pytest
import asyncio
from simplexbot.client import SimplexClient
from simplexbot.command import ShowMyAddress, APICreateGroupLink, APIJoinGroup, APISendMessage, APIGetChats, APIGetChat

@pytest.mark.asyncio
async def test_chat_message_between_two_bots():
    # Connect both bots
    async with SimplexClient("ws://localhost:5225") as bot1, \
               SimplexClient("ws://localhost:5226") as bot2:

        # 1. Get contact links for both bots (SimpleX returns userContactLink)
        await bot1.send_command(ShowMyAddress(), expect_response=False)
        resp1 = await bot1.dequeue()
        assert getattr(resp1.resp, "type", None) == "userContactLink"
        contact_link1 = getattr(resp1.resp, "contact_link", None)
        assert contact_link1 is not None
        conn_req_contact1 = getattr(contact_link1, "conn_req_contact", None)
        assert conn_req_contact1 is not None

        await bot2.send_command(ShowMyAddress(), expect_response=False)
        resp2 = await bot2.dequeue()
        assert getattr(resp2.resp, "type", None) == "userContactLink"
        contact_link2 = getattr(resp2.resp, "contact_link", None)
        assert contact_link2 is not None
        conn_req_contact2 = getattr(contact_link2, "conn_req_contact", None)
        assert conn_req_contact2 is not None

        # 2. Each bot creates a group link (if needed for joining)
        await bot1.send_command(APICreateGroupLink(), expect_response=False)
        link1_resp = await bot1.dequeue()
        assert hasattr(link1_resp.resp, "link")
        link1 = link1_resp.resp.link

        await bot2.send_command(APICreateGroupLink(), expect_response=False)
        link2_resp = await bot2.dequeue()
        assert hasattr(link2_resp.resp, "link")
        link2 = link2_resp.resp.link

        # 3. Bot2 joins Bot1's group using the link
        await bot2.send_command(APIJoinGroup(link=link1), expect_response=False)
        join1 = await bot2.dequeue()
        assert getattr(join1.resp, "ok", True)

        # 4. Bot1 sends a message to the chat
        await bot1.send_command(APIGetChats(), expect_response=False)
        chats = await bot1.dequeue()
        assert hasattr(chats.resp, "chats")
        chat_id = chats.resp.chats[0].chat_id  # Simplified: assumes first chat is the one
        msg_text = "Hello from bot1!"
        await bot1.send_command(APISendMessage(chat_id=chat_id, text=msg_text), expect_response=False)
        send_resp = await bot1.dequeue()
        assert getattr(send_resp.resp, "ok", True)

        # 5. Bot2 receives the message (poll chat)
        await bot2.send_command(APIGetChats(), expect_response=False)
        chats2 = await bot2.dequeue()
        assert hasattr(chats2.resp, "chats")
        chat_id2 = chats2.resp.chats[0].chat_id
        await bot2.send_command(APIGetChat(chat_id=chat_id2), expect_response=False)
        chat = await bot2.dequeue()
        assert any(getattr(item, "text", None) == msg_text for item in getattr(chat.resp, "items", []))

        # 6. Bot2 sends a reply
        reply_text = "Hi bot1, got your message!"
        await bot2.send_command(APISendMessage(chat_id=chat_id2, text=reply_text), expect_response=False)
        send_resp2 = await bot2.dequeue()
        assert getattr(send_resp2.resp, "ok", True)

        # 7. Bot1 receives the reply
        await bot1.send_command(APIGetChat(chat_id=chat_id), expect_response=False)
        chat1 = await bot1.dequeue()
        assert any(getattr(item, "text", None) == reply_text for item in getattr(chat1.resp, "items", []))
