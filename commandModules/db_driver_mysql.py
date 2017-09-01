import MySQLdb as mysql
from datetime import date, datetime
import time
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import config
import pprint

#<editor-fold> DATABASE HELPER FUNCITONS
def connect_mysql():
    connection = mysql.connect(host=config.APP_DB_IP, user=config.APP_DB_USER, password=config.APP_DB_PASS, db=config.APP_DB_DEFAULTDB)
    return connection

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
#</editor-fold>

#<editor-fold> DATABASE OPERATIONS DnD
# Think about adding another DB table that stores attendees of the session
# !attending could return a list of people who are attending, and commands like
# !rsvp or !unrsvp could allow people to reserver or cancel a spot. Author
# can specify the amount of people that can sign up for a session. (Add that into
# create_new_session() and have it affect the new db).
# TODO: Add a new param for new session (max_attending).
def create_new_session(server_id, date, user_id):
    connection = connect_mysql()
    cursor = connection.cursor()
    time_now = datetime.utcnow()
    sql = """
        INSERT INTO dnd_db(server_id, is_active, ts_created, ts_modified, author, set_date)
        VALuES (%s, 1, %s, %s, %s, %s)
        """
    args = [server_id, time_now, time_now, user_id, date]
    cursor.execute(sql, args)
    connection.commit()
    connection.close()

def edit_existing_session(id, server_id, user_id):
    connection = connect_mysql()
    cursor = connection.cursor()
    time_now = datetime.utcnow()

def get_next_session(server_id, user_id):
    connection = connect_mysql()
    cursor = connection.cursor()
    time_now = datetime.utcnow()

#</editor-fold>

#<editor-fold DATABASE OPERATIONS DISCORD/ADMINISTRATIVE
def add_server(server_id, server_alias):
    connection = connect_mysql()
    cursor = connection.cursor()
    time_now = datetime.utcnow()
    sql = """
        INSERT INTO discord_servers(server_id, server_alias, is_active, ts_created, ts_modified)
        VALUES (%s, %s, 1, %s, %s);
        """
    args = [server_id, server_alias, time_now, time_now]
    cursor.execute(sql, args)
    connection.commit()
    connection.close()

def remove_server(server_id):
    connection = connect_mysql()
    cursor = connection.cursor()
    time_now = datetime.utcnow()
    sql = """
        UPDATE discord_servers
            SET is_active = 0,
                ts_modified = %s
        WHERE server_id = %s;
        """
    args = [time_now, server_id]
    cursor.execute(sql, args)
    connection.commit()
    connection.close()

def get_active_servers():
    connection = connect_mysql()
    cursor = connection.cursor()
    sql = """
        SELECT * FROM discord_servers
        WHERE is_active = 1;
    """
    cursor.execute(sql)
    return format_data(cursor)
#</editor-fold>
