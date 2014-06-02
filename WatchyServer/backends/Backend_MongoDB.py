import json
from pymongo import MongoClient

class Backend_Mongo:
    def __init__ (self, uri):
        self.client = MongoClient (uri)

    def consume (self, (key, name, data)):
        data = json.loads (data)
        db = self.client [key]
        db [name].insert (data)
