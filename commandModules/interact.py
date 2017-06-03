import discord
import botMain
import config
from discord.ext import commands
import time
import requests

class Interact():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clap", pass_context=True)
    async def sjw_retarded_clap(self, ctx):
        """ Want to talk like a retarded sjw? Well now you can """

        message = ctx.message.content
        clap = ':clap:'
        split = message.split(' ')
        result_msg = []
        for item in split[1:]:
            result_msg.append(clap)
            result_msg.append(item)
        result_msg.append(clap)
        response = ''.join(map(str, result_msg))
        await self.bot.say('**{}**'.format(response))


def setup(bot):
    bot.add_cog(Interact(bot))
