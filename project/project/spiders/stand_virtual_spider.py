import re
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from project.items import StandVirtualItem


class StandVirtualSpider(Spider):
    name = "standvirtual"
    allowed_domains = ["https://www.standvirtual.com"]

    def start_requests(self):
        url = (
            'https://www.standvirtual.com/'
            'carros/{brand}/?search%5Bnew_used%5D=on'
            .format(brand=self.brand)
        )
        print('url, url')
        yield scrapy.Request(url)

    def parse(self, response):
        ads = Selector(response).xpath(
            '//div[@class="offers list"]/article'
        )

        for ad in ads:
            item = StandVirtualItem()

            item['gas_type'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="fuel_type"]/
                span/
                text()'''
            ).extract()[0]

            item['power'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="power"]/
                span/
                text()'''
            ).extract()[0]

            item['year'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="first_registration_year"]/
                span/
                text()'''
            ).extract()[0]

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

            picture = ad.xpath(
                '''div[@class="offer-item__photo "]/
                a[@class="offer-item__photo-link"]/
                @style''').extract_first()

            # TODO: Make regex more restrict
            item['picture'] = re.search(
                r"'.*'",
                picture
            ).group(0).split("'")[1]

            yield item
