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


import os
import re
import sys
import subprocess
import traceback
from time import time
from io import StringIO
from inspect import getfullargspec

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import OWNER_ID

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message):"
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@Client.on_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
@Client.on_edited_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?**")

    cmd = message.text.split(" ", maxsplit=1)[1]
    start = time()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    redirected_output, redirected_error = StringIO(), StringIO()
    sys.stdout, sys.stderr = redirected_output, redirected_error

    try:
        await aexec(cmd, client, message)
    except Exception:
        error = traceback.format_exc()
    else:
        error = None

    sys.stdout, sys.stderr = old_stdout, old_stderr
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()

    result = error or stderr or stdout or "Success"
    output_text = f"**OUTPUT:**\n```{result.strip()}```"

    if len(output_text) > 4096:
        filename = "output.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result.strip())

        end = time()
        await message.reply_document(
            filename,
            caption=f"**INPUT:**\n`{cmd[:980]}`\n\n**OUTPUT:** `Attached`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏳", callback_data=f"runtime {end - start:.2f} Seconds")]
            ])
        )
        os.remove(filename)
    else:
        end = time()
        await edit_or_reply(
            message,
            text=output_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑", callback_data=f"forceclose abc|{message.from_user.id}")]
            ])
        )


@Client.on_callback_query(filters.regex(r"runtime"))
async def runtime_callback(_, cq):
    try:
        _, runtime = cq.data.split(None, 1)
        await cq.answer(runtime, show_alert=True)
    except Exception:
        pass


@Client.on_callback_query(filters.regex("forceclose"))
async def forceclose_callback(_, callback_query):
    try:
        _, data = callback_query.data.strip().split(None, 1)
        _, user_id = data.split("|")
        if callback_query.from_user.id != int(user_id):
            return await callback_query.answer(
                "» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ʙᴀʙʏ.", show_alert=True
            )
        await callback_query.message.delete()
        await callback_query.answer()
    except:
        pass


@Client.on_message(filters.command("sh") & filters.user(OWNER_ID))
@Client.on_edited_message(filters.command("sh") & filters.user(OWNER_ID))
async def shellrunner(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**ᴇxᴀᴍᴩʟᴇ :**\n/sh git pull")

    text = message.text.split(None, 1)[1]
    if "\n" in text:
        output = ""
        for line in text.split("\n"):
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", line)
            try:
                process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout = process.stdout.read().decode("utf-8").strip()
                output += f"**{line}**\n{stdout}\n"
            except Exception as err:
                return await edit_or_reply(message, text=f"**ERROR:**\n```{err}```")
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        try:
            process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode("utf-8").strip()
        except Exception as err:
            tb = traceback.format_exc()
            return await edit_or_reply(message, text=f"**ERROR:**\n```{tb}```")

    if output:
        if len(output) > 4096:
            with open("output.txt", "w") as f:
                f.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                caption="`Output`",
                reply_to_message_id=message.id,
            )
            os.remove("output.txt")
        else:
            await edit_or_reply(message, text=f"**OUTPUT:**\n```{output}```")
    else:
        await edit_or_reply(message, text="**OUTPUT: **\n`No output`")
