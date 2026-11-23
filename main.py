
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
import time
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)

StartTime = time.time()

async def send_startup_message(client):
    try:
        await client.send_message(
            chat_id=config.OWNER_ID,
            text="البوت يعمل بنجاح! يمكنك استخدامي الان"
        )
        logging.info("تم إرسال رسالة التشغيل إلى المطور بنجاح")
    except Exception as e:
        logging.error(f"فشل في إرسال رسالة التشغيل إلى المطور: {e}")

def main():
    print("تم تشغيل بوت الجلسات بنجاح")
    app = Client(
        name="String-Bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        in_memory=True,
        plugins=dict(root="StringGen"),
    )
    try:
        app.start()
        uname = app.get_me().username
        print(f"ʙᴏᴛ @{uname} ɪꜱ ɴᴏᴡ ʀᴇᴀᴅʏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ꜱᴇꜱꜱɪᴏɴꜱ.")
        app.loop.run_until_complete(send_startup_message(app))

        idle()

    except ApiIdInvalid:
        logging.critical("ɪɴᴠᴀʟɪᴅ ᴀᴘɪ_ɪᴅ ᴏʀ ᴀᴘɪ_ʜᴀꜱʜ. ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏɴꜰɪɢ.")
    except ApiIdPublishedFlood:
        logging.critical("ᴀᴘɪ_ɪᴅ/ʜᴀꜱʜ ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪꜱ ꜰʟᴏᴏᴅ-ʙᴀɴɴᴇᴅ.")
    except AccessTokenInvalid:
        logging.critical("ɪɴᴠᴀʟɪᴅ ʙᴏᴛ_ᴛᴏᴋᴇɴ. ᴘʟᴇᴀꜱᴇ ᴜᴘᴅᴀᴛᴇ ɪᴛ.")
    except Exception as e:
        logging.exception(f"ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ꜱᴛᴀʀᴛᴜᴘ: {e}")
    finally:
        try:
            app.stop()
            print("ꜱᴇꜱꜱɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ ꜱᴛᴏᴘᴘᴇᴅ.")
        except Exception as e:
            logging.error(f"ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ꜱʜᴜᴛᴅᴏᴡɴ: {e}")

if __name__ == "__main__":
    main()