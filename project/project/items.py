from scrapy.item import Item, Field


class StandVirtualItem(Item):
    brand = Field()
    model = Field()
    gas_type = Field()
    power = Field()
    year = Field()
    price = Field()
    picture = Field()
    link = Field()
    title = Field()
    location = Field()
    capacity = Field()
    kms = Field()
