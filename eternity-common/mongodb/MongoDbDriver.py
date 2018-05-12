from pymongo import MongoClient

class MongoDbDriver(object):

    def __init__(self):
        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)

    def get_database(self, database_name):
        return self.client[database_name]


