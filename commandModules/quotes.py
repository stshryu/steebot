import discord
import botMain
import config
from discord.ext import commands
import time
from datetime import date, datetime
import commandModules.db_driver as db

class Quotes():

    def __init__(self, bot):
        self.bot = bot

    def get_quote(self):
        
