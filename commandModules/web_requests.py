import discord
import botMain
import config
from discord.ext import commands
import time
import requests

# steebchamp
from bs4 import BeautifulSoup as bs
import sys
from html.parser import HTMLParser


class Web_Requests():

    def __init__(self, bot):
        self.bot = bot

    ### TODO: This actually gave me an idea, should integrate an OPENDOTA parser
    ### that can get mmr, most played, etc... of players by typing in their username
    ### although you do need Steam32 ID so that may be an issue if you're just typing
    ### in the name instead of the actual ID
    @commands.command(name="nick", pass_context=True)
    async def nick_sucks_at_dota(self, ctx):
        """ Made because honestly, Nick is one of the best Dota players I know """

        # Nick's own personal url to parse his opendota
        request_url = 'https://api.opendota.com/api/players/52926379'
        r = requests.get(request_url)
        if r.status_code == 200:
            data = r.json()
            nick_solo_mmr = int(data['solo_competitive_rank'])
            nick_party_mmr = int(data['competitive_rank'])
            can_nick_play_with_himself = ""
            if nick_solo_mmr - nick_party_mmr > 2000:
                can_nick_play_with_himself = "And no, he cannot diddle his own fiddle"
            else:
                can_nick_play_with_himself = "And yes he can diddle his own fiddle"
            await self.bot.say('Nick\'s solo mmr is: **{}**, his party mmr is: **{}**. {}'.format(nick_solo_mmr, nick_party_mmr, can_nick_play_with_himself))
        else:
            print('Error getting profile')


def setup(bot):
    bot.add_cog(Web_Requests(bot))
