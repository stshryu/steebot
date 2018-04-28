import discord
import botMain
import config
from discord.ext import commands
import time
import requests

# steebchamp ############### CURRENTLY REMOVED #################
# from bs4 import BeautifulSoup as bs
# import sys
# from selenium.webdriver.support.ui import WebDriverWait
# from html.parser import HTMLParser
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

class Web_Requests():

    def __init__(self, bot):
        self.bot = bot

    ######### TODO #########
    # command(steebchamp)
    # Make sure that the webdriver doesnt use chrome (use PhantomJS or some
    # other headless browser). Also see if call can be optimized (takes )
    ########################
    # Gets the last time Steebert played Invoker
    # @commands.command()
    # async def steebchamp(self):
    #     kevin_url = "https://denk-o.github.io/steebchamp.io/"
    #     request_time_start = time.time()
    #     print('Fetching data from steebchamp')
    #     browser = webdriver.Chrome('steebot_env/chromedriver')
    #     browser.get(kevin_url)
    #     button = browser.find_element_by_class_name('btn-invoker')
    #     button.click()
    #     while(True):
    #         html = browser.find_element_by_class_name('text_display').get_attribute('innerHTML').strip(' \t\n\r')
    #         if('Sir' not in html):
    #             continue
    #         else:
    #             last_played_raw = html
    #             browser.close()
    #             break
    #         time.sleep(2)
    #     total_request_time = time.time() - request_time_start
    #     last_played_str = last_played_raw.replace(':', ': ')
    #     print('Request took: {0:.2f} seconds'.format(total_request_time))
    #     print(last_played_str)
    #     await self.bot.say(last_played_str)

    ### TODO: This actually gave me an idea, should integrate an OPENDOTA parser
    ### that can get mmr, most played, etc... of players by typing in their username
    ### although you do need Steam32 ID so that may be an issue if you're just typing
    ### in the name instead of the actual ID
    @commands.command(name="nick", pass_context=True)
    async def nick_sucks_at_dota(self, ctx):
        """ Usage: !nick """

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
