import discord
import asyncio
import commandModules.reminder_mongo as reminder

client = discord.Client()

def background_check_dateTime():
    await client.wait_until_read()
    while not client.is_closed:
        #get top reminder, check top reminder
        handler = reminder_handler()
        r = handler.get_first_reminder()
        send_msg = handler.check_reminder(r)
        await asyncio.sleep(60)
