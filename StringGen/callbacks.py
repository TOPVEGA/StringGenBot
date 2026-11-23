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



import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from StringGen.generate import (
    generate_session,
    ASK_QUES,
    BUTTONS_QUES,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ERROR_MESSAGE = (
    "حدث خطأ غير متوقع أثناء إنشاء الجلسة:\n\n"
    "• يرجى التأكد من إدخال البيانات الصحيحة.\n"
    "• تحقق من صحة API_ID / API_HASH / رقم الهاتف / البوت توكين.\n"
    "• إذا استمرت المشكلة، يرجى التواصل مع الدعم الفني @TOPVEGA"
)

CALLBACK_PATTERN = r"^(generate|pyrogram_v1|pyrogram_v2|pyrogram_bot|telethon|telethon_bot)$"

user_clicks = {}
user_bans = {}

@Client.on_callback_query(filters.regex(CALLBACK_PATTERN))
async def sessiongen_callbacks(bot: Client, cq: CallbackQuery):
    user_id = cq.from_user.id
    current_time = datetime.now()
    if user_id in user_bans:
        if current_time < user_bans[user_id]:
            remaining_time = (user_bans[user_id] - current_time).seconds // 60 + 1
            await cq.answer(f"أنت محظور مؤقتاً لمدة {remaining_time} دقائق بسبب النقر المتكرر", show_alert=True)
            return
        else:
            del user_bans[user_id]
    if user_id not in user_clicks:
        user_clicks[user_id] = {'count': 1, 'time': current_time}
    else:
        time_diff = (current_time - user_clicks[user_id]['time']).seconds
        if time_diff < 60:
            user_clicks[user_id]['count'] += 1
            if user_clicks[user_id]['count'] > 2:
                ban_time = current_time + timedelta(minutes=3)
                user_bans[user_id] = ban_time
                del user_clicks[user_id]
                await cq.answer("تم حظرك مؤقتاً لمدة 3 دقائق بسبب النقر المتكرر", show_alert=True)
                return
        else:
            user_clicks[user_id] = {'count': 1, 'time': current_time}

    choice = cq.data
    try:
        await cq.answer()

        if choice == "generate":
            return await cq.message.reply(
                ASK_QUES,
                reply_markup=InlineKeyboardMarkup(BUTTONS_QUES)
            )

        if choice == "pyrogram_v1":
            return await generate_session(bot, cq.message, old_pyro=True)

        if choice == "pyrogram_v2":
            return await generate_session(bot, cq.message)

        if choice == "pyrogram_bot":
            await cq.answer("جاري إنشاء جلسة بوت Pyrogram...", show_alert=True)
            return await generate_session(bot, cq.message, is_bot=True)

        if choice == "telethon":
            return await generate_session(bot, cq.message, telethon=True)

        if choice == "telethon_bot":
            return await generate_session(bot, cq.message, telethon=True, is_bot=True)

        await cq.message.reply("نوع الجلسة غير معروف.")

    except Exception as e:
        logger.exception(f"حدث خطأ في معالجة الطلب: {e}")
        await cq.message.reply(ERROR_MESSAGE, disable_web_page_preview=True)