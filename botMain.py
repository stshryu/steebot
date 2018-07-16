import discord
import config
from discord.ext import commands
import time
import sched
import asyncio
import itertools

class Bot(commands.Bot):

    start_time = time.time()

    def __init__(self, command_prefix, formatter=None, description=None, pm_help=False, **options):
        super().__init__(command_prefix, formatter, description, pm_help, **options)
        self.initial_config()
        self.initial_extensions()
        self.initial_listener()
        self.create_user_list()

    def initial_config(self):
        self.token = config.Bot_Token
        self.username = config.Bot_Username
        self.app_id = config.App_ID
        self.app_secret = config.App_Secret

    def initial_extensions(self):
        def load_extension(name):
            self.load_extension('commandModules.{0}'.format(name))
        load_extension('web_requests')
        load_extension('util')
        load_extension('reminder_background_checker')
        #load_extension('twitch')
        load_extension('interact')

    def initial_listener(self):
        self.add_listener(self.startup_message, 'on_ready')

    def create_user_list(self):
        self.user_list = []
        gen = self.get_all_members()

    def has_next(iterable):
        try:
            first = next(iterable)
        except StopIteration
            return None
        return first, itertools.chain([first],iterable)
    async def startup_message(self):
        print("Logged in as {}".format(self.username))
        print("Bot ID: {}".format(self.app_id))
        print("-----------")
        self.start_time = time.time()
