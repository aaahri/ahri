import pymongo
from ahri.settings import MONGO


class Mongo:
    def __init__(self, user=MONGO['user'], password=MONGO['pass'], ip=MONGO['host'], port=MONGO['port']):
        self.url = 'mongodb://%s:%s@%s:%s/' % (user, password, ip, port)

    def connect(self):
        return pymongo.MongoClient(self.url)

    def db(self, db):
        return self.connect()[db]

    def col(self, db, collection):
        return self.db(db)[collection]

    def insert(self, collection, document):
        return collection.insert_one(document)
