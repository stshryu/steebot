import discord
import asyncio
import commandModules.reminder_mongo as reminder
import botMain
import config

class reminder_background_checker():
    def __init__(self, bot):
        self.bot = bot
        self.notifier_bg_task = self.bot.loop.create_task(self.checker())
        # self.bg_task = self.bot.loop.create_task(self.botTask())
    async def checker(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            handler = reminder.reminder_handler()
            r = handler.get_first_reminder()
            print(r)
            send_msg = handler.check_reminder(r)
            user = bot.users.get(r.id)
            print(user)
            if user:
                await self.bot.send_message(user, 'askdljfsldjkf');
            if send_msg:
                print('inside if')
                #delete reminder and send the message
                # await client.send_message(r.user, r.message)
                # await self.bot.send_message(r.user_key, r.message)
                print(r)
                handler.delete_first_element()
            await asyncio.sleep(5)
    async def botTask(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            # print('hot second')
            # for attr in dir(self.bot):
            #     if hasattr( self.bot, attr ):
            #         print( "bot.%s = %s" % (attr, getattr(self.bot, attr)))
            # await self.bot.send_message(default_channel, "fuck a duck")
            await asyncio.sleep(10)
        print(self.bot.is_closed)

def setup(bot):
    bot.add_cog(reminder_background_checker(bot))
