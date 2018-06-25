import discord
import botMain
import commandModules.db_driver_sqlite3 as db
import config
from discord.ext import commands
import time
import os

class Utilities():

    def __init__(self, bot):
        self.bot = bot
        self.creator_image = "resources/images/steeb_the_creator.png"

    @commands.command()
    async def runtime(self):
        """ Usage: !runtime """
        current_time = (time.time() - botMain.Bot.start_time)/3600
        print('Bot has been running for: {0:.2f} hours'.format(current_time))
        await self.bot.say('Bot has been running for: **{0:.2f}** hours'.format(current_time))

    @commands.command()
    async def joincommand(self):
        """ Usage: !joincommand """
        join_url = 'https://discordapp.com/oauth2/authorize?client_id=' + config.App_ID + '&scope=bot&permissions=0'
        await self.bot.say('To invite Steebot to your channel go to : {}'.format(join_url))


    @commands.command(name="creator")
    async def owner(self):
        """ Usage: !creator """
        await self.bot.say('My creator is <@' + config.ownerID + ">")
        await self.bot.upload(self.creator_image)

    # On server join add to db
    async def on_server_join(self, server):
        server_id = server.id
        server_name = server.name
        db.add_server(server_id, server_name)
        print('Joined ' + server_name + ' with ID of: ' + server_id)

def setup(bot):
    util = Utilities(bot)
    bot.add_cog(util)
