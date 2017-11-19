from pymongo import MongoClient
import settings


class Database_client(object):
    def __init__(self):
        client = MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = client[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def count(self):
        return {'count': self.collection.count()}

    def all(self):
        data = {}
        documentet_list = []
        for document in self.collection.find():
            document['_id'] = str(document['_id'])
            documentet_list.append(document)

        data['all_cars_list'] = documentet_list;
        return data
