import discord
import botMain
import config
from discord.ext import commands
import time

# steebchamp
from bs4 import BeautifulSoup as bs
import sys
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Web_Requests():

    def __init__(self, bot):
        self.bot = bot

    ######### TODO #########
    # command(steebchamp)
    # Make sure that the webdriver doens't use chrome (use PhantomJS or some
    # other headless browser)
    ########################
    # Gets the last time Steebert played Invoker
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
                browser.close()
                break
            time.sleep(2)
        last_played_str = last_played_raw.replace(':', ': ')
        print(last_played_str)
        await self.bot.say(last_played_str)

def setup(bot):
    bot.add_cog(Web_Requests(bot))
