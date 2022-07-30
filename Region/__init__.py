import os
import logging
import time
import sys
from pyrogram import Client
from redis import Redis
import pyromod.listen

logging.basicConfig(level=logging.INFO)
#Comment
LOGS = logging.getLogger("AnimeBot")
LOGS.setLevel(level=logging.INFO)

#-------------------------------VARS-----------------------------------------
REDIS_URI = os.environ.get("REDIS_URI","redis-16999.c92.us-east-1-3.ec2.cloud.redislabs.com:16999")
REDIS_URI = REDIS_URI.split(":")
REDIS_PASS = os.environ.get("REDIS_PASS","YyYaCkWuBSyme5C6vkYTPk1e4LHenFbW")
BOT_TOKEN = os.environ.get("BOT_TOKEN","5343045120:AAFx4-CSTguKQXWZFUG13mrjuRmk5pUdf60")
API_ID = os.environ.get("API_ID",2663335)
API_HASH = os.environ.get("API_HASH","a4476bdb326701fdadfe834593db59eb")
OWNER = list(filter(lambda x: x, map(int, os.environ.get("OWNER_ID", "5531584953").split())))
#-------------------------------DEFAULT---------------------------------------
TRIGGERS = os.environ.get("TRIGGERS", "/ !").split()
plugins = dict(root="Region/plugin")
#------------------------------CONNECTION------------------------------------
if BOT_TOKEN is not None:
    try:
        pbot = Client("Chizuru", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)
        LOGS.info("❤️ Bot Connected")
    except:
        LOGS.info('😞 Error While Connecting To Bot')    
        sys.exit()            
#-------------------------------DATABASE--------------------------------------------
if REDIS_URI is not None:
    try:
        dB = Redis(
            host=REDIS_URI[0],
            port=REDIS_URI[1],
            password=REDIS_PASS,
            decode_responses=True,
        )
        LOGS.info("❤️ Database Connected")
    except: 
        LOGS.info('😞 Error While Connecting To Database')   
        sys.exit()
