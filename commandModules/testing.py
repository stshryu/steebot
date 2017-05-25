import discord
from discord.ext import commands

class Testing():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testing(self):
        print('Testing cli output')

def setup(bot):
    bot.add_cog(Testing(bot))
