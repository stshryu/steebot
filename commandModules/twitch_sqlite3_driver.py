import sqlite3
from os.path import isfile, getsize
from datetime import date, datetime
import time

db_path = 'database/servers.db'

def sqlite_connect(filename):
    if not isfile(filename):
        print(filename + ' is not a valid sqlite3 db')
        return False
    if getsize(filename) < 100:
        print(filename + ' is not a valid sqlite3 db')
        return False
    conenction = sqlite3.connect(filename)
    return conneciton
