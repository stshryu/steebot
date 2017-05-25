import discord
import botMain
import config
from discord.ext import commands
import time

class Utilities():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def runtime(self):
        current_time = (time.time() - botMain.Bot.start_time)/3600
        print('Bot has been running for: {0:.2f} hours'.format(current_time))
        await self.bot.say('Bot has been running for: **{0:.2f}** hours'.format(current_time))

def setup(bot):
    bot.add_cog(Utilities(bot))
