import os
import play_scraper
from pyrogram import Client, filters
from pyrogram.types import *

Bot = Client(
    "Play-Store-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)



@Client.on_message(filters.command('app') & filters.text)
async def video(client, message):
    app = ["title"]
    results = play_scraper.search(message)
    answers = []
    for result in results:
        details = format(result["title"])
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Play Store", url="https://play.google.com"+result["url"])]]
        ) 
        try:
       
            await message.reply_text(
            text=details,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        except Exception as error:
            print(error)
    await message.reply_text(
    text=details,
    reply_markup=reply_markup,
    disable_web_page_preview=True,
    quote=True
    )
