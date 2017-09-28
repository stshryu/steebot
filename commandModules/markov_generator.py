import discord
import botMain
import config
from discord.ext import commands
import time
import commandModules.message_interface as message_interface
import checks
import commandModules.db_driver_mysql as db
import re

def admin_permission():
    def predicate(ctx):
        if ctx.message.author.id == config.ownerID:
            return True
        try:
            return ctx.message.channel.permissions_for(ctx.message.author).manage_messages
        except:
            return False
    return commands.check(predicate)

class Markov():

    def __init__(self, bot):
        self.bot = bot
        self.message = message_interface.message_handler()

    def does_markov_exist(self, user_id):
        pass
        # Check if user_id is in markov_chain db

    def get_markov_chain(self, user_id):
        pass
        # Return a dictionary/tuple list of the users generated markov chain

    def return_markov_error(self, error_code):
        response = self.message.returnMarkovMsgError(error_code)
        return response

    def return_markov_chain(self, author, message):
        response = self.message.returnMarkovChain(author, message)
        return response

    @commands.command(name="markov", pass_context=True)
    @admin_permission()
    async def imitate(self, ctx):
        """
        Will return a markov chain using your most recent messages imitating you

        Usage: !imitate @OkBread, !imitate <user_id>, !imitate me
        """
        message = ctx.message.content.strip(' ').split(' ')
        user_id = ''
        if len(message) == 1 or len(message) > 2:
            await self.bot.say(self.return_markov_error('Command not invoked properly, too long or too short'))
        elif message[1].casefold() == 'me'.casefold():
            # db.check_markov_data('123', '900') THIS IS THE CHECK TO SEE IF THE MARKOV DATA EXISTS
            user_id = ctx.message.author.id
            # async for msg in self.bot.logs_from(ctx.message.channel, 200):
            #     print(msg.content)
            # await self.bot.say(self.return_markov_chain(user_id, 'Durr hurr'))
        else:
            discord_id_re = r"[<][@]\d+[>]"
            if re.search(discord_id_re, message[1]):
                user_id = message[1][2:-1]
                await self.bot.say(self.return_markov_chain(user_id, 'Durr hurr'))
            else:
                await self.bot.say(self.return_markov_error('Not a valid user'))

        # if(does_markov_exist(user_id)):
        #     markov_chain = get_markov_chain(user_id)
        #     # Do something with chain
        # else:
        #     # Make chain

def setup(bot):
    bot.add_cog(Markov(bot))
