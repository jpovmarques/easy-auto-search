from scrapy.item import Item, Field


class StandVirtualItem(Item):
    title = Field()
    price = Field()
