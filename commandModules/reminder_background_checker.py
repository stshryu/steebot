import discord
import asyncio
import commandModules.reminder_mongo as reminder
import botMain
import config

class reminder_background_checker():
    def __init__(self, bot):
        self.bot = bot
        # self.notifier_bg_task = self.bot.loop.create_task(self.checker())
        self.bg_task = self.bot.loop.create_task(self.botTask())
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
#the below method is a test method
    async def botTask(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            print('loop init')
            handler = reminder.reminder_handler()
            r = handler.get_first_reminder()
            print('------------')
            print(r)
            print('============')
            users = [];
            while True:
                try:
                    item = next(self.bot.user_list)
                except StopIteration:
                    print('aasaas')
                    return
                # if item:
                #     print('ff')
                #     users.append(item)
                # else:
                #     print('hello')
                #     break
            print('sup')
            # for attr in dir(self.bot.user_list):
            #     if hasattr( self.bot.user_list, attr ):
            #         print( "bot.%s = %s" % (attr, getattr(self.bot.user_list, attr)))
            # await self.bot.send_message(default_channel, "fuck a duck")
            await asyncio.sleep(10)
        print(self.bot.is_closed)

def setup(bot):
    bot.add_cog(reminder_background_checker(bot))
