import discord
import botMain
import config
from discord.ext import commands
import time
import commandModules.message_interface as message_interface
import checks
import commandModules.db_driver_mysql as mysql

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

    @commands.command(name="markov", pass_context=True)
    @admin_permission()
    async def imitate(self, ctx):
        """
        Will return a markov chain using your most recent messages imitating you

        Usage: !imitate @OkBread, !imitate <user_id>, !imitate me
        """
        message = ctx.message.content.strip(' ').split(' ')
        user_id = ''
        if len(message) == 1:
            response = self.message.returnMarkovMsgError()
            await self.bot.say(response)
        elif message[1].casefold() == 'me'.casefold():
            user_id = ctx.message.author.id
            async for msg in self.bot.logs_from(ctx.message.channel):
                print(msg.content)
        else:
            user_id = message[1][2:-1]
            print(user_id)

        # if(does_markov_exist(user_id)):
        #     markov_chain = get_markov_chain(user_id)
        #     # Do something with chain
        # else:
        #     # Make chain

def setup(bot):
    bot.add_cog(Markov(bot))
