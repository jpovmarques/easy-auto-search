from scrapy.item import Item, Field


class StandVirtualItem(Item):
    link = Field()
    title = Field()
    price = Field()
    photo = Field()
