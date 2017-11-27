import pprint
from db_client import Database_middleware

db_client = Database_middleware()
pp = pprint.PrettyPrinter(indent=4)


def get_all_brands():
    for item in sorted(db_client.collection.distinct("brand")):
        yield(item)

def get_all_models(brand):
    for item in sorted(db_client.collection.distinct("model", {"brand": brand})):
        yield(item)


def get_all_cars():
    all_cars = {}
    for brand in get_all_brands():
        all_cars[brand.upper()] = [x.upper() for x in get_all_models(brand)]
    return all_cars


[pp.pprint(x.upper()) for x in get_all_brands()]
