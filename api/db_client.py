import json
import settings
from utils import JSONEncoder
from pymongo import MongoClient


class Database_middleware(object):
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
        returns a json with the total number of documents.
        """
        return {'count': self.collection.count()}

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
        returns a json set of documents with the given attributes
        belonging to:
        - page number `page_num` (required)
        - page size `page_size` (required)
        - brand `brand` (optional)
        - model `model` (optional)
        - minimum price `price_min` (optional)
        - maximum price `price_max` (optional)
        - minimum year `year_min` (optional)
        - maximum year `year_max` (optional)
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
        if (not brand and not model and not price_min and not year_min and not year_max): query = {}
        print('debug_query:', query)
        items = self.collection.find(query)
        cursor = items.skip(skips).limit(page_size)
        count = items.count()
        json_response = json.dumps(
            {
                'results_list': [x for x in cursor],
                'results_count': count
            },
            cls=JSONEncoder,
            sort_keys=True,
            indent=4,
        )
        return json_response
