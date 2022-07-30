import os
from datetime import datetime as dt
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from Region.utils.download_handlers import download_from_url
from AnilistPython import Anilist
import pyromod.listen
from Region.utils.anilist_wraper import parser_main
from Region import OWNER as OWNER_ID, pbot as indi
from Region.database.authorize import is_auth
trg = os.environ.get("TRIGGERS", "/ !").split(" ")
anilist = Anilist()

@indi.on_message(filters.command('post', prefixes=trg))
async def post_normal(bot: indi, msg: Message):
    if not (is_auth(msg.from_user.id)):
        await msg.reply('You Are Not Authorized To Perform This Action Contact Admins')
        return
    chat = msg.chat
    anime_name = await bot.ask(chat.id, "Send Anime Name")
    lmao = parser_main(anime_name.text)
    anime_url = lmao[6]
    wallpapers = lmao[2]
    thumb = str(lmao[1])+'.png'
    await download_from_url(wallpapers, thumb)
    links = await bot.ask(chat.id, "Send links")
    print(links.text)
    
    POST_CHANNEL_ID = -1001564668652    
    
    sbuttons = [[InlineKeyboardButton("[𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾 𝗍𝗈 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽]",url = links.text)]]
    
    sucess = await bot.send_photo(POST_CHANNEL_ID,thumb,caption=lmao[4],reply_markup=InlineKeyboardMarkup(sbuttons))  
    await bot.send_message(
        chat.id,
        text = "Successfully Posted",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "View Post",
                        url = sucess.link
                    ),
                ],
            ]
        )
    )
    
    os.remove(thumb)