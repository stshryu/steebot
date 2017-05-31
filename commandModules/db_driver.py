import sqlite3
from os.path import isfile, getsize
from datetime import date, datetime

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
        for index, value in enumerate(row):
            temp_dict = {}
            temp_dict[headers[index]] = value
            temp_arr.append(temp_dict)
        result_data.append(temp_arr)
    return result_data
#</editor-fold>

#<editor-fold> DATABASE OPERATIONS TWITCH
def add_twitch_stream(stream_id, stream_alias):
    connection = sqlite3_connect(db_path)
    cursor = connection.cursor()
    today = date.today()
    sql = """
        INSERT INTO twitch_streams (stream_id, stream_alias, is_active, ts_created, ts_modified)
        VALUES (?, ?, 1, ?, ?);
        """
    cursor.execute(sql, (stream_id, stream_alias, today, today))
    connection.commit()
    connection.close()

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
