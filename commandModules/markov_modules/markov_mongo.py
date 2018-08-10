import pymongo
from pymongo import MongoClient

class markov_handler:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.markov_db
        self.coll = self.db.markov_test_coll
