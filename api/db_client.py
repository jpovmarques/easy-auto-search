import json
from pymongo import MongoClient
import settings


class Database_client(object):
    def __init__(self):
        """
        create a mongodb client instance.
        """
        client = MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = client[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def count(self):
        """
        returns the total number of documents.
        """
        return {'count': self.collection.count()}

    def all(self):
        """
        returns all documents.
        """
        cursor = self.collection.find()
        return {'all_cars_list': [str(x) for x in cursor]}

    def search(self, page_size, page_num, brand=None):
        """
        returns a set of documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        skips = page_size * (page_num - 1)
        if not page_size or not page_num:
            return {'error': 'page size and page number are required params'}

        elif brand:
            cursor = self.collection.find({"brand": brand}).skip(skips).limit(page_size)
            return {'results': [str(x) for x in cursor if x['_id']]}

        cursor = self.collection.find().skip(skips).limit(page_size)
        return {'results': [str(x) for x in cursor if x['_id']]}
