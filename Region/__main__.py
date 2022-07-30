from Region import pbot
import asyncio
import pyromod.listen

pbot.start()
print("Pyrogram Started!")

loop = asyncio.get_event_loop()
loop.run_forever()  