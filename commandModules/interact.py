import discord
import botMain
import config
from discord.ext import commands
import time
import requests
import commandModules.message_interface as message_interface
import checks
import commandModules.db_driver_mysql as mysql

class Interact():

    CONSTANT_CLAP =     'clap'
    CONSTANT_TOILET =   'toilet'

    def __init__(self, bot):
        self.bot = bot
        self.message = message_interface.message_handler()

    @commands.command(name="clap", pass_context=True)
    async def sjw_retarded_clap(self, ctx):
        """ Want to talk like a retarded sjw? Well now you can with !clap """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.createEmojiMessage(author, message, Interact.CONSTANT_CLAP)
        await self.bot.say(response)

    @commands.command(name="toilet", pass_context=True)
    #@checks.is_owner() #do stuff with this later
    async def toilet(self, ctx):
        """ The magical toilet """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.createEmojiMessage(author, message, Interact.CONSTANT_TOILET)
        await self.bot.say(response)

    @commands.command(name="timclap", pass_context=True)
    async def timclap(self, ctx):
        """ Want to be a retard like Ryan, Gary, and Kevin? Well now you can with !timclap """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.returnTimClap(author)
        await self.bot.say(response)

    @commands.command(name="steebclap", pass_context=True)
    async def steebclap(self, ctx):
        """ Want to be a retard like kevin? Well now you can with !steebclap """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.returnSteebClap(author)
        await self.bot.say(response)

    @commands.command(name="steebclap2", pass_context=True)
    async def steebclap2(self, ctx):
        """ Want to be a retard like Ryan? Well now you can with !steebclap2 """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.returnSteebClap(author, 1)
        await self.bot.say(response)

    @commands.command(name="steebclap3", pass_context=True)
    async def steebclap2(self, ctx):
        """ Want to be a retard like Steebert? Well now you can with !steebclap3 """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.returnSteebClap(message, author, 2)
        await self.bot.say(response)


    @commands.command(name="cowsay", pass_context=True)
    async def cowsay(self, ctx):
        """ Cowsay functionality """

        message = str(ctx.message.content)
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message.returnCowsay(message, author)
        await self.bot.say(response)

def setup(bot):
    bot.add_cog(Interact(bot))
