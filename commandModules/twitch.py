import discord
import botMain
import config
from discord.ext import commands
import time
from datetime import date, datetime
import commandModules.db_driver as db
import requests
import asyncio
import pprint

def twitch_permission():
    def predicate(ctx):
        if ctx.message.author.id == config.ownerID:
            return True
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
    multi_stream_param = 'streams?'

    def __init__(self, bot):
        self.bot = bot
        self.twitch_id = config.Twitch_ClientID

        self.notifier_lock = asyncio.Lock()
        self.notifier_bg_task = bot.loop.create_task(self.twitch_notifier())

    def __del__(self):
        self.notifier_bg_task.cancel()

    #<editor-fold> Twitch helper functions
    ## TODO maybe add a funciton that takes an array of values and outputs to the
    ## bot.say command to make changing the notificaiton message easier
    ## e.g. def notifier_thing(self, msg_type, param)... or something like that
    ## Check Zon's bot for an example of formatted messages (probably easier to edit too)

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

    def get_default_channel_obj(self, server_id):
        server = self.bot.get_server(str(server_id))
        return server.default_channel

    def chunks(self, list_, chunk_size):
        """Yield successive n-sized chunks from a list."""

        for i in range(0, len(list_), chunk_size):
            yield list_[i:i + chunk_size]

    def get_live_stream_by_chunk(self, stream_arr, update=True):
        """ Automatically chunks requests into arrays of 100 and queries Twitch """

        # Get 50 streams per request from Twitch
        twitch_stream_url = 'https://twitch.tv/'
        stream_chunked = self.chunks(stream_arr, 50)
        live_streams = []
        live_stream_metadata = {}
        for streams in stream_chunked:
            concat_stream_url = ','.join(streams)
            request_url = self.TWITCH_BASE_URL + self.multi_stream_param + 'channel=' + concat_stream_url + '&client_id=' + self.twitch_id
            pp.pprint(request_url) ## DEBUGGING
            r = requests.get(request_url)
            if r .status_code == 200:
                data = r.json()
                online_streams_raw = data['streams']
                for stream in online_streams_raw:
                    temp_dict = {}
                    temp_dict['title'] = stream['channel']['status']
                    temp_dict['game'] = stream['game']
                    temp_dict['twitch_url'] = twitch_stream_url + str(stream['channel']['name'])
                    live_stream_metadata[stream['channel']['name']] = temp_dict
            live_streams.append(live_stream_metadata)
            pp.pprint('Currently live streams: {}'.format(live_stream_metadata)) ## DEBUGGING
            live_stream_diff = []
            diff = []
            for stream in live_streams:
                for key, value in stream.items():
                    diff.append(key)
                    temp = []
                    temp.append(key)
                    temp.append('1')
                    live_stream_diff.append(temp)
            streams_diff = list(set(streams) - set(diff))
            for item in streams_diff:
                temp = []
                temp.append(item)
                temp.append('0')
                live_stream_diff.append(temp)
            db_diff = db.get_all_stream_status()['results'][0]
            db_stream_diff = []
            for item in db_diff:
                temp = []
                temp.append(item[0]['stream_alias'])
                temp.append(item[0]['is_online'])
                db_stream_diff.append(temp)
            comp_live = []
            comp_db = []
            for item in live_stream_diff:
                comp_live.append(str(item[0]) + ':' + str(item[1]))
            for item in db_stream_diff:
                comp_db.append(str(item[0]) + ':' + str(item[1]))
            twitch_stream_diff = list(set(comp_live) - set(comp_db))
            update_stream = []
            for item in twitch_stream_diff:
                update_stream.append(item.split(':'))
            # query = db.update_live_streams(update_stream)
            result = {}
            result['live_streams'] = update_stream
            result['live_stream_metadata'] = live_stream_metadata
            pp.pprint('Return query is here: {}'.format(result)) ## DEBUGGING
            return result
            # if(query):
            #     return update_stream
            # else:
            #     return False

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
        print(stream_diff_live) ## DEBUG
        print(stream_diff_db) ## DEBUG
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
                temp_arr.append(item[0]['ts_modified'])
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

    @commands.command(name="following", pass_context=True)
    @twitch_permission()
    async def get_followed_streams(self, ctx):
        """ Display all currently followed Twitch Streams on server """
        server_id = ctx.message.server.id
        stream_aliases = self.get_followed_stream_aliases(server_id)
        if(len(stream_aliases)>0):
            message = []
            message.append('```Currently Following on this Server:\n')
            for stream in stream_aliases:
                stream_ = stream[0] + ',\n'
                message.append(stream_)
            message.append('```')
            response = ''.join(map(str, message))
            await self.bot.say(response)
        else:
            await self.bot.say('Not following any streams on this server. If you want to add a stream type:\n `!twitch follow <stream>`')

    @twitch.command(name="add", pass_context=True)
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
                is_followed = db.is_stream_followed(server_id, stream_alias)
                if(is_followed):
                    print('Error: StreamID: {} already followed by ServerID {}'.format(stream_id, server_id))
                    await self.bot.say('Error: **{}** is already being followed.'.format(stream_alias))
                else:
                    query = db.follow_twitch_stream(server_id, stream_alias)
                    if(query):
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

    @twitch.command(name="remove", pass_context=True)
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

    async def twitch_notifier(self):
        """ Notifications for followed Twitch Streams
        Should note that I took a lot of this code from Zonbot to learn about asyncio
        events in Python

        Also send_message() requires a channel object not just the channel ID
        """

        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            async with self.notifier_lock:
                data = db.get_all_active_twitch_subs()
                results = data['results']
                streams = []
                for stream in results[0]:
                    streams.append(stream[0]['stream_alias'])
                stream_data = self.get_live_stream_by_chunk(streams)
                live_streams = stream_data['live_streams']
                stream_metadata = stream_data['live_stream_metadata']
                live_parsing = []
                for item in live_streams:
                    live_parsing.append(item[0])
                servers = db.get_all_servers()
                pp.pprint('Current time is: {}'.format(datetime.utcnow())) ## DEBUGGING
                pp.pprint('Live parsing stuff is here: {}'.format(live_parsing)) # DEBUGGING
                for server in servers:
                    server_id = server[0]['id']
                    default_channel = self.get_default_channel_obj(server_id)
                    stream_aliases = self.get_followed_stream_aliases(server_id)
                    for item in stream_aliases:
                        ts_modified = item[2]
                        split = ts_modified.split(' ')
                        date_split = split[0].split('-')
                        time_split = split[1].split(':')
                        now_utc = datetime.utcnow()
                        year = int(date_split[0].lstrip('0'))
                        month = int(date_split[1].lstrip('0'))
                        day = int(date_split[2].lstrip('0'))
                        hour = int(time_split[0].lstrip('0'))
                        minute = int(time_split[1].lstrip('0'))
                        last_modified = datetime(year, month, day, hour, minute)
                        last_notified = int((now_utc - last_modified).total_seconds()/60)
                        if item[0] in live_parsing and item[1] == 0:
                            name = item[0]
                            title = stream_metadata[name]['title']
                            game = stream_metadata[name]['game']
                            twitch_url = stream_metadata[name]['twitch_url']
                            if(last_notified > 15):
                                await self.bot.send_message(default_channel, '**{}** is now playing **{}**: {} at <{}>'.format(name, game, title, twitch_url))
                db.update_live_streams(live_streams)
            await asyncio.sleep(60)
    #</editor-fold>

def setup(bot):
    bot.add_cog(Twitch(bot))
