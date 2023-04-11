import os
import requests
import weasyprint
import urllib.request
from plugins.helpers.presets import Presets
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from plugins.helpers.config import Config

# -------------------------- Bot Configuration ---------------------------------------------- #
Bot = Client(
    "link2PdfBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
)


# ------------------------------ Start Command ---------------------------------------------- #


# -------------------------------- Main execution fn --------------------------------------- #
@Client.on_message(filters.private & filters.text)
async def link_extract(self, m: Message):
    if not m.text.startswith("http"):
        await m.reply_text(
            Presets.INVALID_LINK_TXT,
            reply_to_message_id=m.message_id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_data")]]
            )
        )
        return
    file_name = str()
    #
    thumb_path = os.path.join(os.getcwd(), "img")
    if not os.path.isdir(thumb_path):
        os.makedirs(thumb_path)
        urllib.request.urlretrieve(Presets.THUMB_URL, os.path.join(thumb_path, "thumbnail.png"))
    else:
        pass
    #
    thumbnail = os.path.join(os.getcwd(), "img", "thumbnail.png")
    #
    await self.send_chat_action(m.chat.id, "typing")
    msg = await m.reply_text(Presets.PROCESS_TXT, reply_to_message_id=m.message_id)
    try:
        req = requests.get(m.text)
        # using the BeautifulSoup module
        soup = BeautifulSoup(req.text, 'html.parser')
        # extracting the title frm the link
        for title in soup.find_all('title'):
            file_name = str(title.get_text()) + '.pdf'
        # Creating the pdf file
        weasyprint.HTML(m.text).write_pdf(file_name)
    except Exception:
        await msg.edit_text(
            Presets.ERROR_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_data")]]
            )
        )
        return
    try:
        await msg.edit(Presets.UPLOAD_TXT)
    except Exception:
        pass
    await self.send_chat_action(m.chat.id, "upload_document")
    await m.reply_document(
        document=file_name,
        caption=Presets.CAPTION_TXT.format(file_name),
        thumb=thumbnail
    )
    print(
        '@' + m.from_user.username if m.from_user.username else m.from_user.first_name,
        "has downloaded the file",
        file_name
    )
    try:
        os.remove(file_name)
    except Exception:
        pass
    await msg.delete()


# --------------------------------- Close Button Call Back --------------------------------- #
