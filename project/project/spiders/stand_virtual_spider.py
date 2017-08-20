import re
from scrapy import Spider
from scrapy.selector import Selector
from project.items import StandVirtualItem


class StandVirtualSpider(Spider):
    name = "standvirtual"
    allowed_domains = ["https://www.standvirtual.com"]
    start_urls = [
        "https://www.standvirtual.com/carros/bmw/?search%5Bnew_used%5D=on"
    ]

    def parse(self, response):
        ads = Selector(response).xpath(
            '//div[@class="offers list"]/article'
        )

        for ad in ads:
            item = StandVirtualItem()

            item['link'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                div[@class="offer-item__title"]/
                h2[@class="offer-title"]/
                a[@class="offer-title__link"]/
                @href'''
            ).extract()[0]

            item['title'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                div[@class="offer-item__title"]/
                h2[@class="offer-title"]/
                a[@class="offer-title__link"]/
                @title'''
            ).extract()[0]

            item['price'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                div[@class="offer-item__price"]/
                div[@class="offer-price"]/
                span[@class="offer-price__number"]/
                text()'''
            ).extract()[0].rstrip()

            photo = ad.xpath(
                ''' div[@class="offer-item__photo "]/
                a[@class="offer-item__photo-link"]/
                @style''').extract_first()

            item['photo'] = re.search(r"'.*'", photo).group(0).split("'")[1]

            yield item
