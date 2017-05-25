import discord
import botMain
import config
from discord.ext import commands

# required for status
import time

# required for steebchamp
from bs4 import BeautifulSoup as bs
import sys
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Testing():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self):
        current_time = (time.time() - botMain.Bot.start_time)/3600
        print('Bot has been running for: {0:.2f} hours'.format(current_time))
        await self.bot.say('Bot has been running for: **{0:.2f}** hours'.format(current_time))

    @commands.command()
    async def steebchamp(self):
        kevin_url = "https://denk-o.github.io/steebchamp.io/"
        request_time_start = time.time()
        print('Fetching data from steebchamp')
        browser = webdriver.Chrome('steebot_env/chromedriver')
        browser.get(kevin_url)
        button = browser.find_element_by_class_name('btn-invoker')
        button.click()
        while(True):
            html = browser.find_element_by_class_name('text_display').get_attribute('innerHTML').strip(' \t\n\r')
            if('Sir' not in html):
                continue
            else:
                last_played_raw = html
                break
            time.sleep(2)
        print(last_played_raw)
        await self.bot.say(last_played_raw)

def setup(bot):
    bot.add_cog(Testing(bot))
