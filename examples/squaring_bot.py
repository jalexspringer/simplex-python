"""
Squaring Bot Example

A simple bot that responds to numbers by calculating their square.
This is the Python equivalent of the TypeScript squaring-bot.js example.
"""

import asyncio
from simplexbot.client import SimplexClient
from simplexbot.command import (
    ChatType,
)

SERVER_URL = "ws://localhost:5225"
WELCOME_MSG = "Hello! I am a simple squaring bot - if you send me a number, I will calculate its square"


async def main():
    # Connect to the chat server
    async with SimplexClient(SERVER_URL) as client:
        # Check if we have an active user
        user = await client.get_active_user()
        if not user:
            print("No user profile")
            return
            
        # Extract user profile information
        display_name = user["profile"]["displayName"] if isinstance(user, dict) else user.profile.display_name
        full_name = user["profile"].get("fullName", "") if isinstance(user, dict) else getattr(user.profile, "full_name", "")
        print(f"Bot profile: {display_name} ({full_name})")
        
        # Get or create the user address
        address = await client.get_user_address() or await client.create_user_address()
        if not address:
            print("Could not get or create bot address.")
            return
        print(f"Bot address: {address}")
        
        # Enable automatic acceptance of contact connections
        await client.enable_address_auto_accept()
        
        # Process incoming messages
        async for event in client.events():
            event_type = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
            
            # Handle contact connected event
            if event_type == "contactConnected":
                contact = event["contact"] if isinstance(event, dict) else event.contact
                contact_id = contact["contactId"] if isinstance(contact, dict) else contact.contact_id
                contact_name = (contact["profile"]["displayName"] 
                               if isinstance(contact, dict) 
                               else contact.profile.display_name)
                print(f"{contact_name} connected")
                
                # Send welcome message
                await client.send_text_message(
                    ChatType.DIRECT,
                    contact_id,
                    WELCOME_MSG
                )
                
            # Handle new chat items
            elif event_type == "newChatItems":
                chat_items = event["chatItems"] if isinstance(event, dict) else event.chat_items
                
                for item in chat_items:
                    # Extract chat info and item content
                    chat_info = item["chatInfo"] if isinstance(item, dict) else item.chat_info
                    chat_item = item["chatItem"] if isinstance(item, dict) else item.chat_item
                    
                    # Only process direct messages
                    chat_type = chat_info["type"] if isinstance(chat_info, dict) else chat_info.type
                    if chat_type != "direct":
                        continue
                    
                    # Extract the message text
                    content = chat_item["content"] if isinstance(chat_item, dict) else chat_item.content
                    if isinstance(content, dict) and content.get("type") == "rcvMsgContent":
                        msg_content = content.get("msgContent", {})
                        if isinstance(msg_content, dict) and msg_content.get("type") == "text":
                            text = msg_content.get("text", "")
                        else:
                            continue
                    else:
                        continue
                    
                    # Try to parse the number and calculate square
                    try:
                        n = float(text)
                        reply = f"{n} * {n} = {n * n}"
                    except ValueError:
                        reply = "This is not a number"
                    
                    # Send the response
                    contact = chat_info["contact"] if isinstance(chat_info, dict) else chat_info.contact
                    contact_id = contact["contactId"] if isinstance(contact, dict) else contact.contact_id
                    await client.send_text_message(
                        ChatType.DIRECT,
                        contact_id,
                        reply
                    )


if __name__ == "__main__":
    asyncio.run(main())
