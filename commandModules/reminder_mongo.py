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
        r = {
            'user': user,
            'message': msg,
            'current_date': datetime.datetime.utcnow(),
            'reminder_date': reminder_date
        }
        #TODO: Rate limit insertion operation to n times
        r_id = self.coll.insert_one(r).inserted_id
        #after every insert we sort to make getting the db easier
        self.coll.find().sort([('reminder_date', pymongo.ASCENDING)])
        return r_id

    def check_reminder(self, reminder):
        #peek the top level element of db and pop it if it's time
        current_time = datetime.datetime.utcnow().replace(second=0,microsecond=0)
        #using find_one get the top level element of sorted array
        next_reminder = reminder
        next_reminder_date = next_reminder.get('reminder_date')

        pop_reminder = True if current_time == next_reminder_date else False
        print(next_reminder.get('reminder_date'))
        return pop_reminder

    def delete_first_element(self):
        #delete the first element of db
        #ONLY CALL THIS METHOD AFTER CHECKING_REMINDER
        self.coll.delete();

    def get_first_reminder(self):
        #more helper methods idk why i do this
        return self.coll.find_one()
k = reminder_handler()
print(k.check_reminder(k.get_first_reminder()))
