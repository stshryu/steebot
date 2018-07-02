#another db interface b/c me n steeb have no fucking clue what we're doing
import pymongo
import datetime
from pymongo import MongoClient

# client = MongoClient()
# db = client.test_database
# coll = db.test_collection
#
# reminder = {
#     'user': 'testUser',
#     'message': 'hello world',
#     'date': datetime.datetime.utcnow()
# }
#
# posts = db.posts
# post_id = posts.insert_one(reminder).inserted_id


class db_handler:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.reminder_db
        self.coll = self.db.reminders

    def insert_reminder(self, user, msg):
        r = {
            'user': user,
            'message': msg,
            'date': datetime.datetime.utcnow()
        }
        print('hit this')
        r_id = self.coll.insert_one(r).inserted_id

        return r_id
testdb = db_handler()
testdb.insert_reminder('testuser', 'test message')
