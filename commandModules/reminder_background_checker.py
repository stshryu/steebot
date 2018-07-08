import discord
import asyncio
import commandModules.reminder_mongo as reminder
import botMain
import config

class reminder_background_checker():
    def __init__(self, bot):
        self.bot = bot
        self.notifier_bg_task = bot.loop.create_task(self.checker())
    async def checker(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            handler = reminder.reminder_handler()
            r = handler.get_first_reminder()
            send_msg = handler.check_reminder(r)
            if send_msg:
                #delete reminder and send the message
                # await client.send_message(user, reminder)
                await self.bot.send_message(r.user, r.message)
                print(r)
                handler.delete_first_element()
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(reminder_background_checker(bot))
