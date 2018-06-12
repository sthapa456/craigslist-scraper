 #
 # 
 # Copyright (C) 2018 Raymond Wai Yan Ko <wisely38@hotmail.com>
 #
 # 
 # This file is part of craigslist-scraper.
 # 
 # craigslist-scraper cannot be copied and/or distributed for commercial use 
 # without the express permission of Raymond Wai Yan Ko <wisely38@hotmail.com>
 #
 #

from pymongo import MongoClient


class MongoDbDriver(object):

    def __init__(self):
        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)

    def get_database(self, database_name):
        return self.client[database_name]
