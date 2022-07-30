import datetime
import html
import json
from async_timeout import timeout
import requests
from requests import get
import datetime
import requests
from datetime import datetime as dt
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
url = 'https://graphql.anilist.co'

OKANY = False
def parser_main(query):
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
        genre_d = json['genres']
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
        return anime_name_w, anime_id, image, description, msgd, trailer, info, genre_d