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


class reminder_handler:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.reminder_db
        self.coll = self.db.reminders

    def insert_reminder(self, user, msg, reminder_date):
        r_date = reminder_date if reminder_date else "empty"
        print(r_date)
        r = {
            'user': user,
            'message': msg,
            'current_date': datetime.datetime.utcnow(),
            'reminder_date': reminder_date
        }
        print('hit this')
        r_id = self.coll.insert_one(r).inserted_id
        self.coll.find().sort({'reminder_date':1})
        return r_id
testdb = reminder_handler()
testdb.insert_reminder('testuser', 'test message', 'aa')
