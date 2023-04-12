import os
import requests
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()

REMOVEBG_API = "xncwdQU8EBAW7KQK9fK9CgTK"
UNSCREEN_API = "1pWrEXF6pTmNyuMjbgghvbW4"

Bot = Client(
    "Remove Background Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)



BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Join Channel', url='https://telegram.me/nasrani_update')
        ]
    ]
)










@Client.on_message(filters.command("bg") & (filters.photo | filters.video | filters.document))
async def remove_background(bot, update):
    
    try:
        new_file_name = f"./{str(update.from_user.id)}"
        if (
            update.photo or (
                update.document and "image" in update.document.mime_type
            )
        ):
            new_file_name += ".png"
            file = await update.download()
            await message.edit_text(
                text="Photo downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_image(file)
        elif (
            update.video or (
                update.document and "video" in update.document.mime_type
            )
        ):
            new_file_name += ".webm"
            file = await update.download()
            await message.edit_text(
                text="Video downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_video(file)
        else:
            await message.edit_text(
                text="Media not supported",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
        try:
            os.remove(file)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=error,
            disable_web_page_preview=True
        )
    try:
        with open(new_file_name, "wb") as file:
            file.write(new_document.content)
        await update.reply_chat_action("upload_document")
    except Exception as error:
        await message.edit_text(
           text=error,
           reply_markup=ERROR_BUTTONS
        )
        return
    try:
        await update.reply_document(
            document=new_file_name,
            quote=True
        )
        try:
            os.remove(new_file_name)
        except:
            pass
    except Exception as error:
        await message.reply_text(
            text=f"Error:- `{error}`",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )


def removebg_video(file):
    return requests.post(
        "https://api.unscreen.com/v1.0/videos",
        files={"video_file": open(file, "rb")},
        headers={"X-Api-Key": UNSCREEN_API}
    )


