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
from typing import Union
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden
from config import OWNER_ID
from StringGen.save_user import save_user
from StringGen.database import users
from StringGen.database import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cairo_tz = pytz.timezone('Africa/Cairo')

def command_filter(cmd: Union[str, list]) -> filters.Filter:
    return filters.private & filters.incoming & filters.command(cmd)

async def is_user_joined(bot: Client, user_id: int) -> bool:
    try:
        await bot.get_chat_member("vegaone", user_id)
        return True
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat @vegaone!")
        return False
    except Exception as e:
        logger.exception(f"Error checking user membership: {e}")
        return False

async def notify_developer(bot: Client, user):
    try:
        user_info = (
            f"• وافد جديد يطرق أبواب البوت:\n\n"
            f"• هويته الرقمية: `{user.id}`\n"
            f"• اسمه: {user.first_name}\n"
            f"• لقبه: @{user.username}\n"
            f"• رقمه: {user.phone_number if user.phone_number else 'غير مسجل'}"
        )

        await bot.send_message(
            chat_id=OWNER_ID,
            text=user_info,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.exception("عذراً، لم نتمكن من إبلاغ المطور:")

@Client.on_message(filters.private & filters.incoming)
async def must_join_channel(bot: Client, msg: Message):
    if msg.from_user.is_bot:
        return

    if not "vegaone":
        return

    if not await is_user_joined(bot, msg.from_user.id):
        if "vegaone".isalpha():
            link = "https://t.me/vegaone"
        else:
            try:
                chat_info = await bot.get_chat("vegaone")
                link = chat_info.invite_link
            except Exception as e:
                link = "https://t.me/vegaone"

        try:
            await msg.reply(
                f"<b>• تحية طيبة يا {msg.from_user.mention}\n• لا يمكنك المضي قدمًا قبل الانضمام إلى قناتنا\n• تفضل بالانضمام: @vegaone ثم عاود المحاولة</b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("انضم الآن", url=link)]
                ])
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
        return

    await msg.continue_propagation()

@Client.on_message(command_filter(["start", "help"]))
async def start_handler(bot: Client, message: Message):
    if not await is_user_joined(bot, message.from_user.id):
        return

    user = message.from_user
    await save_user(user)

    try:
        await notify_developer(bot, user)

        bot_info = await bot.get_me()
        bot_name = bot_info.first_name or "هذا البوت"

        if bot_info.photo:
            photo = await bot.download_media(bot_info.photo.big_file_id)
        else:
            photo = None

        existing = await users.find_one({"_id": user.id})
        join_info = "VeGaCHatt"
        if existing and "joined" in existing:
            join_time = existing["joined"]
            if isinstance(join_time, datetime):
                cairo_time = join_time.astimezone(cairo_tz)
                join_info = f"\n• توقيت القاهرة حين انضمامك: **{cairo_time.strftime('%d-%m-%Y %I:%M %p')}**"

        response_text = (
            f"<b>• أهلاً وسهلاً بك أيها العزيز {user.mention}\n\n"
            f"• أنا **{bot_name}**، بين يديك\n"
            "• أساعدك في استخراج جلسات Pyrogram أو Telethon أو Bot بكل يسر وسهولة.\n"
            "• من صنع يد المبدع: @TopVeGa"
            f"{join_info}\n\n"
            "• اضغط على **الزر أدناه** لتبدأ رحلتك مع الجلسات </b>"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("إنشاء جلسة جديدة", callback_data="generate")],
            [
                InlineKeyboardButton("الدعم والمساعدة", url="https://t.me/vegaone"),
                InlineKeyboardButton("المطور", url="https://t.me/TopVeGa")
            ]
        ])

        if photo:
            await message.reply_photo(
                photo=photo,
                caption=response_text,
                reply_markup=keyboard,
                show_caption_above_media=True
            )
        else:
            await message.reply_text(
                text=response_text,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

    except Exception as e:
        logger.exception("حدث خلل أثناء تشغيل /start أو /help:")
        await message.reply_text(
            "عذراً، طرأ خطأ غير متوقع. نرجو معاودة المحاولة فيما بعد."
        )