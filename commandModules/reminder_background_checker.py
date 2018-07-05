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
        if send_msg:
            #delete reminder and send the message
            handler.delete_first_element()

        await asyncio.sleep(60)
