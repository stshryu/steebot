import discord
import asyncio
import commandModules.reminder_mongo as reminder
import botMain
import config

class reminder_background_checker():
    def __init__(self, bot):
        self.bot = bot
        self.notifier_bg_task = self.bot.loop.create_task(self.checker())

        #testing method: deprecate later
        # self.bg_task = self.bot.loop.create_task(self.botTask())
    async def checker(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            handler = reminder.reminder_handler()
            r = handler.get_first_reminder()
            print(r)
            if r:
                if r.get('id'):
                    #only delete message if send_msg true
                    send_msg = handler.check_reminder(r)
                    user = await self.bot.get_user_info(r.get('id'))
                    if send_msg:
                        print('inside if')
                        await self.bot.send_message(user, r.get('message'));
                        print('send this')
                        print(r)
                        handler.delete_first_element()
                        print('successful delete')
            await asyncio.sleep(60)
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
            print(r.get('id'))
            user = await self.bot.get_user_info(r.get('id'))
            await self.bot.send_message(user, 'FUCK')
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
