import discord
import botMain
import config
from discord.ext import commands
import time
import commandModules.db_driver as db
import requests

def twitch_permission():
        def predicate(ctx):
            if ctx.message.channel.is_private: return True
            try:
                return ctx.message.channel.permissions_for(ctx.message.author).manage_messages
            except:
                return False
        return commands.check(predicate)

class Twitch():
    TWITCH_BASE_URL = 'https://api.twitch.tv/kraken/'
    stream_param = 'streams/'
    channel_param = 'channels/'

    def __init__(self, bot):
        self.bot = bot
        self.twitch_id = config.Twitch_ClientID

    #<editor-fold> Twitch helper functions
    ## TODO maybe add a funciton that takes an array of values and outputs to the
    ## bot.say command to make changing the notificaiton message easier
    ## e.g. def notifier_thing(self, msg_type, param)... or something like that

    # If stream exists returns information on it (if doesn't exist returns false)
    def verify_stream(self, stream_alias, stream_request=False):
        if not stream_request:
            request_url = Twitch.TWITCH_BASE_URL + Twitch.channel_param + stream_alias + '?client_id=' + self.twitch_id
        else:
            request_url = Twitch.TWITCH_BASE_URL + Twitch.stream_param + stream_alias + '?client_id=' + self.twitch_id
        r = requests.get(request_url)
        if r.status_code == 200:
            return r.json()
        else:
            return False

    def is_stream_followed(self, server_id, stream_alias):
        if(db.is_stream_followed(server_id, stream_alias)):
            return True
        else:
            return False

    def get_live_streams(self, stream_arr, update=True):
        twitch_stream_url = 'https://twitch.tv/'
        stream_arr = stream_arr
        stream_diff_db = []
        live_streams = []
        live_stream_metadata = {}
        offline = 0
        online = 0
        for item in stream_arr:
            stream_diff_db.append(item[0] + ':' + str(item[1]))
        for stream in stream_arr:
            stream_name = stream[0]
            temp_arr = []
            temp_arr.append(stream[0])
            request_url = Twitch.TWITCH_BASE_URL + Twitch.stream_param + str(stream_name) + '?client_id=' + self.twitch_id
            r = requests.get(request_url)
            if r.status_code == 200:
                data = r.json()
                if data['stream'] == None:
                    offline = offline + 1
                    temp_arr.append('0')
                else:
                    online = online + 1
                    temp_dict = {}
                    temp_dict['title'] = data['stream']['channel']['status']
                    temp_dict['game'] = data['stream']['game']
                    live_stream_metadata[stream_name] = temp_dict
                    temp_arr.append('1')
            live_streams.append(temp_arr)
        # If we want all live streams regardless of last DB status
        if not update:
            all_live_streams = []
            for item in live_stream_metadata:
                temp_dict = {}
                temp_dict['name'] = item
                temp_dict['title'] = live_stream_metadata[item]['title']
                temp_dict['game'] = live_stream_metadata[item]['game']
                temp_dict['twitch_url'] = twitch_stream_url + item
                all_live_streams.append(temp_dict)
            return all_live_streams
        stream_diff_live = []
        for item in live_streams:
            stream_diff_live.append(item[0] + ':' + str(item[1]))
        # Returns the live value of the stream status into stream_diff
        stream_diff = list(set(stream_diff_live) - set(stream_diff_db))
        update_stream = []
        for item in stream_diff:
            temp_split = item.split(':')
            temp_arr = []
            temp_arr.append(temp_split[0])
            temp_arr.append(temp_split[1])
            update_stream.append(temp_arr)
        output_stream = []
        for item in update_stream:
            if item[1] == '1':
                temp_dict = {}
                temp_dict['name'] = item[0]
                temp_dict['twitch_url'] = twitch_stream_url + item[0]
                temp_dict['title'] = live_stream_metadata[item[0]]['title']
                temp_dict['game'] = live_stream_metadata[item[0]]['game']
                output_stream.append(temp_dict)
        query = db.update_live_streams(update_stream)
        if(query['results']):
            print('Successfully wrote to DB: {}/{} stream[s] online. {}/{} stream[s] offline'.format(online, len(stream_arr), offline, len(stream_arr)))
        return output_stream

    def get_followed_stream_ids(self, server_id):
        server_id = server_id
        print('Getting followed streams for ServerID: {}'.format(server_id))
        followed_streams = db.get_followed_streams_id(server_id)
        stream_ids = []
        if(len(followed_streams) > 0):
            for item in followed_streams['results']:
                stream_ids.append(item[0]['stream_id'])
        print('Found {} streams followed by ServerID: {}'.format(len(stream_ids), server_id))
        return stream_ids

    def unfollow_stream(self, server_id, stream_alias):
        query = db.unfollow_stream(server_id, stream_alias)
        if(query):
            return True
        else:
            return query['errors']

    def get_followed_stream_aliases(self, server_id):
        server_id = server_id
        print('Getting followed streams for ServerID: {}'.format(server_id))
        followed_streams = db.get_followed_streams_aliases(server_id)
        stream_aliases = []
        if(len(followed_streams) > 0):
            for item in followed_streams['results']:
                temp_arr = []
                temp_arr.append(item[0]['stream_alias'])
                temp_arr.append(item[0]['is_online'])
                stream_aliases.append(temp_arr)
        print('Found {} streams followed by ServerID: {}'.format(len(stream_aliases), server_id))
        return stream_aliases

    def get_stream_data(self, stream_array):
        """ Takes an array of stream_aliases to parse from Twitch """
        stream_metadata = []
        for stream in stream_array:
            stream_data = self.verify_stream(stream)
            stream_metadata.appned(stream_data)
        return stream_metadata

    #</editor-fold>

    #<editor-fold> Twitch Commands
    @commands.group(pass_context=True, invoke_without_command=True)
    async def twitch(self, ctx, stream : str):
        """ Checks if stream exists, and if stream is streaming

        Usage: !twitch <stream_name>
        """
        stream_data = self.verify_stream(stream, True)
        if not stream_data:
            print('Not a valid stream: {}'.format(stream))
            await self.bot.say('**{}** is not a valid Twitch.tv Stream'.format(stream))
        else:
            if stream_data['stream'] == None:
                print('{} is offline'.format(stream))
                await self.bot.say('**{}** is currently offline'.format(stream))

    @twitch.command(name="test", pass_context=True)
    @twitch_permission()
    async def testing(self, ctx):
        print('help a me')

    @commands.command(name="refresh", pass_context=True)
    async def refresh_followed_streams(self, ctx):
        """ Force refresh on all followed streams on a server (notifier cron does the same thing). """
        server_id = ctx.message.server.id
        # stream_ids = self.get_followed_stream_ids(server_id) stream id's not used in twitch???
        stream_aliases = self.get_followed_stream_aliases(server_id)
        live_streams = self.get_live_streams(stream_aliases)
        for item in live_streams:
            await self.bot.say('**{}** is now playing **{}**: {} at {}'.format(item['name'], item['game'], item['title'], item['twitch_url']))

    @commands.command(name="live", pass_context=True)
    async def live_followed_streams(self, ctx):
        """ Gets all live streams followed by a server. """
        server_id = ctx.message.server.id
        stream_aliases = self.get_followed_stream_aliases(server_id)
        all_live_streams = self.get_live_streams(stream_aliases, False)
        for item in all_live_streams:
            await self.bot.say('**{}** is currently playing **{}**: {} at {}'.format(item['name'], item['game'], item['title'], item['twitch_url']))

    @twitch.command(name="follow", pass_context=True)
    @twitch_permission()
    async def add_twitch_stream(self, ctx, stream : str):
        """ Adds twitch stream to db (if it does not exist) then follows stream and updates """
        print('Checking if stream {} exists on Twitch...'.format(stream))
        data = self.verify_stream(stream)
        if(data):
            server_id = ctx.message.server.id
            stream_alias = data['name']
            stream_id = str(data['_id'])
            print('Stream {} exists on Twitch'.format(stream_alias))
            # If exists in db don't add, just follow
            if(db.does_twitch_stream_exist(int(stream_id))):
                print('StreamID: {}. Exists in db'.format(stream_id))
                query = db.follow_twitch_stream(server_id, stream_alias)
                if(len(query['errors'])):
                    for item in query['errors']:
                        if('exists' in item):
                            print('Error: StreamID: {} already followed by ServerID {}'.format(stream_id, server_id))
                            await self.bot.say('Error: **{}** is already being followed.'.format(stream_alias))
                        else:
                            print('Error: \"{}\" returned.'.format(item))
                            await self.bot.say('Error: **\"{}\"** returned.'.format(item))
                else:
                    print('ServerID: {} successfully followed StreamID: {}'.format(server_id, stream_id))
                    await self.bot.say('Successfully followed: **{}**.'.format(stream_alias))
            # If doens't exist in db, add then follow
            else:
                print('StreamID: {} does not exist. Adding to DB now...'.format(stream_id))
                query = db.add_twitch_stream(stream_id, stream_alias)
                if(len(query['errors'])):
                    for item in query['errors']:
                        print('Error: \"{}\" returned.'.format(item))
                        await self.bot.say('Error: **\"{}\"** returned.'.format(item))
                else:
                    print('StreamID: {} added to DB'.format(stream_id))
                    query = db.follow_twitch_stream(server_id, stream_alias)
                    if(len(query['errors'])):
                        await self.bot.say('Error: **\"{}\"** returned.'.format(item))
                    else:
                        print('ServerID: {} successfully followed StreamID: {}'.format(server_id, stream_id))
                        await self.bot.say('Successfully followed: **{}**.'.format(stream_alias))
        else:
            print('Twitch stream {} not found'.format(stream))
            await self.bot.say('Twitch Error: Stream for **{}** not found'.format(stream))

    @twitch.command(name="unfollow", pass_context=True)
    @twitch_permission()
    async def remove_twitch_stream(self, ctx, stream : str):
        """ Unfollows stream from DB """
        server_id = ctx.message.server.id
        print('Unfollowing {} on ServerID: {}'.format(stream, server_id))
        if not self.is_stream_followed(server_id, stream):
            print('Stream: {} is not followed on ServerID: {}'.format(stream, server_id))
            await self.bot.say('Error: **{}** is not followed on this server'.format(stream))
        else:
            result = self.unfollow_stream(server_id, stream)
            if(result):
                print('Stream: {} was successfully unfollowed on ServerID: {}'.format(stream, server_id))
                await self.bot.say('Successfully removed **{}**'.format(stream))
            else:
                for item in result:
                    print(item)
                await self.bot.say('Unknown error occured while removing {}'.format(stream))
    #</editor-fold>

def setup(bot):
    bot.add_cog(Twitch(bot))
