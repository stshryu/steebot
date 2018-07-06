import discord
import asyncio
import reminder_mongo as reminder

client = discord.Client()

print('hello')
async def background_check_dateTime():
    print('fff')
    while not client.is_closed:
        #get top reminder, check top reminder
        handler = reminder_handler()
        r = handler.get_first_reminder()
        print(r)
        send_msg = handler.check_reminder(r)
        if send_msg:
            #delete reminder and send the message
            # await client.send_message(user, reminder)
            handler.delete_first_element()

        await asyncio.sleep(60)
