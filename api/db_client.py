import json
import settings
from pymongo import MongoClient


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

    def search(
            self,
            page_size,
            page_num,
            brand=None,
            model=None,
            price_min=None,
            price_max=None,
            year_min=None,
            year_max=None
            ):
        """
        returns a set of documents with the given attributes
        belonging to page number `page_num`
        where size of each page is `page_size`.
        """
        skips = page_size * (page_num - 1)
        condition_list = []
        if brand: condition_list.append({ "brand": brand })
        if model: condition_list.append({ "model": model })
        if price_min: condition_list.append({ "price": { "$gt": price_min } })
        if price_max: condition_list.append({ "price": { "$lt": price_max } })
        if year_min: condition_list.append({ "year": { "$gt": year_min } })
        if year_max: condition_list.append({ "year": { "$lt": year_max } })

        query = { "$and": condition_list }
        print('query:', query)
        cursor = self.collection.find(query).skip(skips).limit(page_size)
        return {'results': [str(x) for x in cursor if x['_id']]}
