import aiohttp
import aiofiles
import os
import time

from Chizuru import LOGS as LOG
async def download_from_url(url, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as out:
            file = await aiofiles.open(name, "wb")
            await file.write(await out.read())
            await file.close()
    return 