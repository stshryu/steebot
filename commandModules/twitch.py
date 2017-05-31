import discord
import botMain
import config
from discord.ext import commands
import time
import commandModules.db_driver as db

# Example request to see if stream exists:
# https://api.twitch.tv/kraken/channels/ohhhmyyy?client_id=dicks
# Request to see if stream is online:
# https://api.twitch.tv/kraken/streams/ohhhmyyy?client_id=dicks

class Twitch():
    twitch_base_url = 'https://api.twitch.tv/kraken/'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addstream")
    async def add_twitch_stream(self, stream : str):

    # Debugging command to list all servers
    @commands.command()
    async def servers(self):
        for item in self.bot.servers:
            print(item.id)

def setup(bot):
    bot.add_cog(Twitch(bot))
