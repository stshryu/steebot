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
        """ Want to talk like a retarded sjw? Well now you can with !clap """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        clap = ':clap:'
        split = message.split(' ')
        result_msg = []
        for item in split[1:]:
            result_msg.append(clap)
            result_msg.append(item)
        result_msg.append(clap)
        response = ''.join(map(str, result_msg))
        await self.bot.say('**{}** said: **{}**'.format(author, response))

    @commands.command(name="steebclap", pass_context=True)
    async def steebclap(self, ctx):
        """ What to be a retard like kevin? Well now you can with !steebclap """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        message = ':clap:don\'t:clap:pretend:clap:to:clap:be:clap:an:clap:OkBread:clap:unless:clap:you:clap:poop:clap:uncontrollably:clap:'
        await self.bot.say('**{}** says: **{}**'.format(author, message))

    @commands.command(name="test", pass_context=True)
    async def testing(self, ctx):
        print(ctx.message.author)

def setup(bot):
    bot.add_cog(Interact(bot))
