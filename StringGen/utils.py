# © VEGA — Intellectual Property Rights

# Respect for Copyright and Content Protection

# In this project, we are committed to respecting community laws, protecting intellectual property rights, and appreciating the efforts of all creators and content owners.

# "All rights are reserved to their original owners, and this project does not constitute a waiver of any intellectual property rights belonging to other parties.

# © VEGA — All rights related to this project are reserved to their owners."

# Supporting Creators is a Responsibility

# - Creativity is the fruit of effort that deserves appreciation and respect.
# - Protecting copyright contributes to building a more just digital community.
# - Usage licenses and redistribution terms must be respected.
# - We reject unauthorized use of any content protected by copyright.

# Responsible Use Pledge

# By using this project, you pledge to respect intellectual property rights and not to copy or redistribute any protected content without obtaining the necessary permission or license.

# Be a partner in protecting creativity, and do not be a cause of rights violations.

# © VEGA | By: @TopVeGa All Rights Reserved



import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio.exceptions import TimeoutError

pending_users = {}

async def ask(client: Client, user_id: int, text: str, timeout: int = 60) -> Message:
    await client.send_message(user_id, text)

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending_users[user_id] = future

    try:
        return await asyncio.wait_for(future, timeout)
    except TimeoutError:
        pending_users.pop(user_id, None)
        await client.send_message(user_id, "⌛ ᴛɪᴍᴇᴏᴜᴛ. ᴄᴀɴᴄᴇʟʟɪɴɢ...")
        raise
    except Exception:
        pending_users.pop(user_id, None)
        raise

@Client.on_message(filters.private & filters.text)
async def listen_for_reply(bot: Client, message: Message):
    future = pending_users.pop(message.chat.id, None)
    if future and not future.done():
        future.set_result(message)
