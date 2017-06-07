import sqlite3
from os.path import isfile, getsize
from datetime import date, datetime
import time

db_path = 'database/servers.db'

#<editor-fold> DATABASE HELPER FUNCTIONS
# Returns a connection object to the db specified in db_path
def sqlite3_connect(filename):
    if not isfile(filename):
        print(filename + ' is not a valid sqlite3 db')
        return False
    if getsize(filename) < 100:
        print(filename + ' is not a valid sqlite3 db')
        return False
    connection = sqlite3.connect(filename)
    return connection

# Returns formatted data from database as an list of dictionaries with {col_name: value}
def format_data(cursor_object):
    cursor = cursor_object
    raw_data = cursor.fetchall()
    headers_raw = cursor.description
    headers = []
    for row in headers_raw:
        headers.append(row[0])
    result_data = []
    for row in raw_data:
        temp_arr = []
        temp_dict = {}
        for index, value in enumerate(row):
            temp_dict[headers[index]] = value
        temp_arr.append(temp_dict)
        result_data.append(temp_arr)
    return result_data
#</editor-fold>

#<editor-fold> DATABASE OPERATIONS TWITCH
def update_live_streams(streams):
    start_time = time.time()
    stream_alias = []
    stream_online = []
    stream_offline = []
    for index, value in enumerate(streams):
        if value[1] == '0':
            stream_offline.insert(index, value[0])
        else:
            stream_online.insert(index, value[0])
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    result = {}
    result['results'] = []
    result['errors'] = []
    placeholder = '?'
    placeholders = ', '.join(placeholder for unused in stream_offline)
    # Update streams that went online first
    sql_offline = """
        UPDATE twitch_streams
            SET is_online = 0
        WHERE stream_alias IN ( %s );
        """ % placeholders
    # Update streams that went online
    placeholder = '?'
    placeholders = ', '.join(placeholder for unused in stream_online)
    sql_online = """
        UPDATE twitch_streams
            SET is_online = 1
        WHERE stream_alias IN ( %s );
        """ % placeholders
    try:
        if(len(sql_offline) > 0):
            cursor.execute(sql_offline, stream_offline)
            connection.commit()
        if(len(sql_online) > 0):
            cursor.execute(sql_online, stream_online)
            connection.commit()
        result['results'].append(True)
    except:
        result['errors'].append('Error: Could not update stream status')
    connection.close()
    print('Query Runtime: {} seconds'.format(time.time() - start_time))
    return result

def get_all_stream_status():
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        SELECT stream_alias, is_online FROM twitch_streams
        WHERE is_active = 1;
        """
    try:
        cursor.execute(sql)
        result['results'].append(format_data(cursor))
    except Exception as e:
        result['errors'].append(e)
    connection.close()
    return result

def get_all_active_twitch_subs():
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        SELECT DISTINCT stream_alias FROM twitch_subs
        WHERE is_active = 1;
        """
    try:
        cursor.execute(sql)
        result['results'].append(format_data(cursor))
    except Exception as e:
        result['errors'].append(e)
    connection.close()
    return result

def add_twitch_stream(stream_id, stream_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        INSERT INTO twitch_streams (stream_id, stream_alias, is_active, ts_created, ts_modified)
        VALUES (?, ?, 1, ?, ?);
        """
    try:
        cursor.execute(sql, (stream_id, stream_alias, today, today))
        connection.commit()
        result['results'].append(True)
    except sqlite3.IntegrityError:
        result['errors'].append('Error: Entry alredy exists')
    connection.close()
    return result

def remove_twitch_stream(stream_id):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    sql = """
        UPDATE twitch_streams
            SET is_active = 0 ,
                ts_modified = ?
        WHERE stream_id = ?;
        """
    cursor.execute(sql, (today, stream_id))
    connection.commit()
    connection.close()
    return True

def does_twitch_stream_exist(stream_id):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        SELECT * FROM twitch_streams
        WHERE stream_id = ?
        """
    cursor.execute(sql, (stream_id,))
    result['results'] = format_data(cursor)
    if(len(result['results'])):
        return True
    else:
        return False

def follow_twitch_stream(server_id, stream_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        UPDATE twitch_subs
            SET is_active = 1,
                ts_modified = ?
        WHERE server_id = ? and stream_alias = ?;
        """
    sql2 = """
        INSERT INTO twitch_subs (server_id, stream_alias, is_active, ts_created, ts_modified)
        SELECT ?, ?, 1, ?, ?
        WHERE (Select Changes() = 0);
        """
    try:
        cursor.execute(sql, (today, server_id, stream_alias))
        cursor.execute(sql2, (server_id, stream_alias, today, today))
        connection.commit()
        result['results'].append(True)
    except sqlite3.IntegrityError:
        result['errors'].append('Error: Entry alredy exists')
    connection.close()
    return result

def unfollow_stream(server_id, stream_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        UPDATE twitch_subs
            SET is_active = 0,
                ts_modified = ?
        WHERE server_id = ? and stream_alias = ?;
        """
    try:
        cursor.execute(sql, (today, server_id, stream_alias))
        connection.commit()
        results['results'].append(True)
    except:
        result['errors'].append('Error: Stream unfollow failed')
    connection.close()
    return result

def is_stream_followed(server_id, stream_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        SELECT * FROM twitch_subs
        WHERE server_id = ? and stream_alias = ? and is_active = 1;
        """
    cursor.execute(sql, (server_id, stream_alias))
    result['results'] = format_data(cursor)
    if(len(result['results'])):
        return True
    else:
        return False

def get_followed_streams_id(server_id):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    sql = """
        SELECT * FROM twitch_subs
        WHERE server_id = ? and is_active = 1;
        """
    try:
        cursor.execute(sql, (server_id,))
        result['results'] = format_data(cursor)
    except:
        result['errors'].append('Error: Error getting followed streams')
    connection.close()
    return result

def get_followed_streams_aliases(server_id):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    result = {}
    result['results'] = []
    result['errors'] = []
    ##### Deprecated with the use of stream_alias instead of stream_id
    ##### if for some reason stream_id needs to be used, uncomment this sql statement
    # sql = """
    #     SELECT twitch_subs.is_online, twitch_streams.stream_alias, twitch_subs.server_id FROM twitch_subs
    #     INNER JOIN twitch_streams ON twitch_streams.stream_id = twitch_subs.stream_id
    #     WHERE twitch_subs.server_id = ?;
    #     """
    sql = """
        SELECT twitch_subs.server_id, twitch_streams.is_online, twitch_subs.stream_alias FROM twitch_subs
        INNER JOIN twitch_streams on twitch_streams.stream_alias = twitch_subs.stream_alias
        WHERE server_id = ? AND twitch_subs.is_active = 1;
        """
    try:
        cursor.execute(sql, (server_id,))
        result['results'] = format_data(cursor)
    except:
        result['errors'].append('Error: Error getting followed streams')
    connection.close()
    return result

def get_active_streams():
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    sql = """
        SELECT * FROM twitch_streams
        WHERE is_active = 1;
        """
    cursor.execute(sql)
    return format_data(cursor)
#</editor-fold>

#<editor-fold> DATABASE OPERATIONS DISCORD/ADMINISTRATIVE
def add_server(server_id, server_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    sql = """
        INSERT INTO discord_servers (id, server_alias, is_active, ts_created, ts_modified)
        VALUES (?, ?, 1, ?, ?);
        """
    cursor.execute(sql, (server_id, server_alias, today, today))
    connection.commit()
    connection.close()

def remove_server(server_id):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    sql = """
        UPDATE discord_servers
            SET is_active = 0 ,
                ts_modified = ?
        WHERE id = ?;
        """
    cursor.execute(sql, (today, server_id))
    connection.commit()
    connection.close()

# Active servers in DB (maybe redundant since you can get this information from the bot anyways)
def get_active_servers():
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    sql = """
        SELECT * FROM discord_servers
        WHERE is_active = 1;
        """
    cursor.execute(sql)
    return format_data(cursor)

# Get all severs that added Steebot at one point or another
def get_all_servers():
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    sql = """
        SELECT * FROM discord_servers
        """
    cursor.execute(sql)
    return format_data(cursor)
#</editor-fold>
