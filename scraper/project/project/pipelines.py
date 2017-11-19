from pymongo import MongoClient
from scrapy.conf import settings
from scrapy import log
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    def __init__(self):
        client = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            log.msg("Item added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
