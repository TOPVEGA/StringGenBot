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




import tempfile
from datetime import timedelta, timezone
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
from StringGen.database import users

IST = timezone(timedelta(hours=5, minutes=30))

@Client.on_message(filters.command("احصائيات","") & filters.user(OWNER_ID))
async def stats_handler(_, message: Message):
    total = await users.count_documents({})
    await message.reply_text(f"إجمالي المستخدمين: `{total}`")

@Client.on_message(filters.command("شيير","") & filters.user(OWNER_ID))
async def broadcast_handler(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("طريقة الاستخدام: `/broadcast رسالتك هنا`")

    text = message.text.split(None, 1)[1]
    success, failed = 0, 0

    async for user in users.find({}, {"_id": 1}):
        try:
            await bot.send_message(user["_id"], text)
            success += 1
        except Exception:
            failed += 1

    await message.reply_text(
        f"اكتمل البث.\n\n"
        f"تم التوصيل: `{success}`\n"
        f"فشل: `{failed}`"
    )

@Client.on_message(filters.command("المستخدمين","") & filters.user(OWNER_ID))
async def users_list(bot: Client, message: Message):
    lines = []
    count = 0

    async for user in users.find().sort("joined", -1):
        uid = user["_id"]
        name = user.get("name", "غير متوفر")
        username = user.get("username", "غير متوفر")
        joined = user.get("joined")
        if joined:
            join_time = joined.astimezone(IST)
            join_info = join_time.strftime('%d-%m-%Y %I:%M %p') + " توقيت الهند"
        else:
            join_info = "غير معروف"

        lines.append(f"{uid} • {name} (@{username}) — انضم: {join_info}")
        count += 1

    total = await users.count_documents({})

    if count <= 50:
        reply_text = "المستخدمون المسجلون:\n\n"
        reply_text += "\n".join([f"• `{line}`" for line in lines])
        reply_text += f"\n\nالإجمالي: `{total}`"
        await message.reply_text(reply_text)
    else:
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as file:
            file.write("\n".join(lines))
            file.seek(0)
            await message.reply_document(
                file.name,
                caption=f"إجمالي المستخدمين: `{total}`"
            )