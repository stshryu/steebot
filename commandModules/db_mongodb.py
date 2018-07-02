#another db interface b/c me n steeb have no fucking clue what we're doing
import pymongo
import datetime
from pymongo import MongoClient

client = MongoClient()
db = client.test_database
coll = db.test_collection

reminder = {
    'user': 'testUser',
    'message': 'hello world',
    'date': datetime.datetime.utcnow()
}

posts = db.posts
post_id = posts.insert_one(reminder).inserted_id

def initialize():
    self.client = MongoClient()
    self.db = client.reminder_db
    self.coll = db.reminders

def insert_reminder(user, msg):
    r = {
        'user': user,
        'message': msg,
        'date': datetime.datetime.utcnow()
    }

    r_id = self.coll.inesert_one(r).inserted_id

    print(r_id)
insert_reminder('asdf', 'test routine');
