from scrapy.item import Item, Field


class StandVirtualItem(Item):
    brand = Field()
    model = Field()
    serie = Field()
    version = Field()
    gas_type = Field()
    power = Field()
    capacity = Field()
    lotation = Field()
    color = Field()
    year = Field()
    kms = Field()
    price = Field()
    picture = Field()
    link = Field()
    title = Field()
    location = Field()
