import datetime
import html
import textwrap
import json
from async_timeout import timeout
import bs4
import requests
import pyromod.listen
from requests import get
import  datetime
import os, requests
from datetime import datetime as dt
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from Region.utils.download_handlers import download_from_url
from Region import pbot as indi, OWNER as OWNER_ID
from Region.database.authorize import is_auth

anime_query = """
query ($id: Int, $idMal:Int, $search: String, $type: MediaType, $asHtml: Boolean) {
  Media (id: $id, idMal: $idMal, search: $search, type: $type) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    description (asHtml: $asHtml)
    startDate {
      year
      month
      day
    }
    season
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
      thumbnail
    }
    coverImage {
      extraLarge
    }
    bannerImage
    genres
    averageScore
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    isAdult
    characters (role: MAIN, page: 1, perPage: 10) {
      nodes {
        id
        name {
          full
          native
        }
        image {
          large
        }
        description (asHtml: $asHtml)
        siteUrl
      }
    }
    studios (isMain: true) {
      nodes {
        name
        siteUrl
      }
    }
    siteUrl
  }
}
"""

url = 'https://graphql.anilist.co'
trg = os.environ.get("TRIGGERS", "/ !").split(" ")
OKANY = False


def refresh_parser(query):
    search = query
    if OKANY is True:
        return
    else:
        search = search
    variables = {'search': search, 'type': "ANIME"}

    if search.isdigit():
        variables = {'id': int(search), 'type': "ANIME"}
        
    json = requests.post(
        url, json={
            'query': anime_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        return
    if json:
        json = json['data']['Media']
        msgd = f"**{json['title']['english']}** | **{json['title']['romaji']}**\n\n**‣ Type**: `{json['format']}`\n**‣ Status**: `{json['status']}`\n**‣ Episodes**: `{json.get('episodes', 'N/A')}`\n**‣ Duration**: `{json.get('duration', 'N/A')} Per Ep.`\n**‣ Score**: `{json['averageScore']}`\n**‣ Genres**: `"
        for x in json['genres']:
            msgd += f"{x}, "
        msgd = msgd[:-2] + '`\n'
        msgd += "**‣ Studios**: `"
        for x in json['studios']['nodes']:
            msgd += f"{x['name']}, "
        msgd = msgd[:-2] + '`\n'
        anime_name_w = f"{json['title']['english']}"
        anime_name_j = json['title']['romaji']         
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A')
        image = f"https://img.anili.st/media/{anime_id}"
        return msgd, description

def call_back_in_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data in query.data,
        data=data
    )



@indi.on_message(filters.command('chs', prefixes=trg))
async def post_normal(bot: indi, msg: Message):
    if not (is_auth(msg.from_user.id)):
        await msg.reply('You Are Not Authorized To Perform This Action Contact Admins')
        return
    search = await bot.ask(msg.chat.id, "ANIME NAME")
    search = search.text
    if OKANY is True:
        return
    else:
        search = search
    variables = {'search': search, 'type': "ANIME"}
    
    if search.isdigit():
        variables = {'id': int(search), 'type': "ANIME"}
        
    json = requests.post(
        url, json={
            'query': anime_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        bot.send_message(msg.chat.id, "error")
        return
    if json:
        json = json['data']['Media']
        msgd = f"**{json['title']['english']}** | **{json['title']['romaji']}**\n\n**‣ Type**: `{json['format']}`\n**‣ Status**: `{json['status']}`\n**‣ Episodes**: `{json.get('episodes', 'N/A')}`\n**‣ Duration**: `{json.get('duration', 'N/A')} Per Ep.`\n**‣ Score**: `{json['averageScore']}`\n**‣ Genres**: `"
        for x in json['genres']:
            msgd += f"{x}, "
        msgd = msgd[:-2] + '`\n'
        msgd += "**‣ Studios**: `"
        for x in json['studios']['nodes']:
            msgd += f"{x['name']}, "
        msgd = msgd[:-2] + '`\n'
        anime_name_w = f"{json['title']['english']}"
        anime_name_j = json['title']['romaji']         
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A')
        image = f"https://img.anili.st/media/{anime_id}"
        channel_id = await bot.ask(msg.chat.id, "Kidhar Post Krna Hai Be")
        channel_id  = int(channel_id.text)
        coverImg = json.get('coverImage')['extraLarge']
        await download_from_url(image, 'temp.png')
        await download_from_url(coverImg, 'channeltemp.png')
        photo_set = await bot.set_chat_photo(channel_id, photo='channeltemp.png')
        
        POST_CHANNEL_ID = "https://t.me/AnimeRegion"
            
        if trailer:
            okays = await bot.send_photo(
            channel_id,
            caption=msgd,
            photo='temp.png',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Trailer 🎬", url=trailer),
                        InlineKeyboardButton("More Info", url=info)
                    ],
                    [
                        InlineKeyboardButton('Refresh', callback_data='fk')
                    ]
                ],
            ),
        )
        else:
            okays = await bot.send_photo(
            channel_id,
            caption=msgd,
            photo='temp.png',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("More Info", url=info)
                    ],
                    [
                        InlineKeyboardButton('Refresh', callback_data='fk')
                    ]
                ],
            ),
        )    
            
                  
        
        await bot.send_sticker(channel_id, "sticker.webp")
        await bot.send_message(channel_id, description,
                               reply_markup=InlineKeyboardMarkup(
                                   [
                                       [
                                           InlineKeyboardButton(
                                               "Anime Info",
                                               url = okays.link
                                           ),
                                           InlineKeyboardButton(
                                               "Our Channels",
                                               url = POST_CHANNEL_ID
                                           )
                                       ]
                                   ]
                               ))
        await bot.send_sticker(channel_id, "sticker.webp")
        
        await bot.send_message(msg.chat.id,text = "Successfully Posted",reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton("View Post", url = okays.link)]]))
        return msgd
         
        
        
@indi.on_callback_query(call_back_in_filter("fk"))
def callbackk(_,query):
    
    text2 = query.message.caption.split('\n\n')
    text2 = text2[0].split("|")
    if 'None' in text2[0]:
        text2 = text2[1]
    else:
        text2 = text2[0]   
        
    lmao = refresh_parser(text2)
    lmao  = lmao[0]      

    if query.data == "fk":
        time_ = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")


        try:
            query.message.edit(lmao, 
                               reply_markup=InlineKeyboardMarkup(
        [    
            query.message.reply_markup.inline_keyboard[0],
            query.message.reply_markup.inline_keyboard[1],

        ],
        
            
        ))
            query.answer("Refreshed!")


        except:
            query.answer("Already Up-To-Date")        