import discord
import botMain
import config
from discord.ext import commands
import time
import requests
import commandModules.message_interface as message_interface
import checks
import commandModules.db_driver_mysql as mysql
import commandModules.reminder_mongo as reminder
import toolkit.toolkit as toolkit

class Interact():

    CONSTANT_CLAP =     'clap'
    CONSTANT_TOILET =   'toilet'

    def __init__(self, bot):
        self.bot = bot
        self.toolkit = toolkit.toolkit()
        self.remind = reminder.reminder_handler()
        self.message_interface = message_interface.message_handler()
        self.steeb_the_bear_img = "resources/images/steeb_the_sad_bear.png"
        self.steeb_the_bear_caption = "resources/images/steeb_the_sad_bear_caption.png"

    @commands.command(name="clap", pass_context=True)
    async def sjw_retarded_clap(self, ctx):
        """ Usage: !clap <message> """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.createEmojiMessage(author, message, Interact.CONSTANT_CLAP)
        await self.bot.say(response)

    @commands.command(name="toilet", pass_context=True)
    #@checks.is_owner() #do stuff with this later
    async def toilet(self, ctx):
        """ Usage: !toilet <message> """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.createEmojiMessage(author, message, Interact.CONSTANT_TOILET)
        await self.bot.say(response)

    @commands.command(name="timclap", pass_context=True)
    async def timclap(self, ctx):
        """ Usage: !timclap """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.returnTimClap(author)
        await self.bot.say(response)

    @commands.command(name="steebclap", pass_context=True)
    async def steebclap(self, ctx):
        """ Usage: !steebclap """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.returnSteebClap(author)
        await self.bot.say(response)

    @commands.command(name="steebclap2", pass_context=True)
    async def steebclap2(self, ctx):
        """ Usage: !steebclap2 """

        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.returnSteebClap(author, 1)
        await self.bot.say(response)

    @commands.command(name="steebclap3", pass_context=True)
    async def steebclap3(self, ctx):
        """ Usage: !steebclap3 """

        message = ctx.message.content
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.returnSteebClap(author, 2)
        await self.bot.say(response)


    @commands.command(name="cowsay", pass_context=True)
    async def cowsay(self, ctx):
        """ Usage: !cowsay -h for detailed help """

        message = ctx.message.content
        message = message.replace('\n', ' ')
        author_ = ctx.message.author
        author = str(author_).split('#')[0]
        response = self.message_interface.returnCowsay(message, author)
        await self.bot.say(response)

    @commands.command(name="roll", pass_context=True)
    async def roll(self, ctx):
        """ Usage: !roll <x-y> """

        message = ctx.message.content
        _author = ctx.message.author
        author = str(_author).split('#')[0]
        response = self.message_interface.returnRoll(message, author)
        await self.bot.say(response)

    @commands.command(name="steebbear", pass_context=True)
    async def steebear(self, ctx):
        """ Usage: !steebbear """

        await self.bot.upload(self.steeb_the_bear_caption)
    @commands.command(name ="reminder", pass_context=True)
    async def reminder(self, ctx):
        """ Usage: !reminder <"message"> <duration>"""

        payload = self.toolkit.commandStripper(ctx.message.content).split('"')
        message = payload[1]
        date = payload[2]
        _author = ctx.message.author
        author = str(_author)
        res = self.remind.insert_reminder(author,message,date)
        if res:
            bot_response = 'Reminder Saved'
        else:
            bot_response = 'Failed to Save'
        await self.bot.say(bot_response)

def setup(bot):
    bot.add_cog(Interact(bot))
