import re
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from project.items import StandVirtualItem


class StandVirtualSpider(Spider):
    name = "standvirtual"
    allowed_domains = ["https://www.standvirtual.com"]

    '''start_urls = (
        'https://www.standvirtual.com/carros/BMW/?search%5Bnew_used%5D=on',
    )'''

    def start_requests(self):
        url = (
            'https://www.standvirtual.com/'
            'carros/{brand}/?search%5Bnew_used%5D=on'
            .format(brand=self.brand)
        )
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        print('parse')

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

            link = ad.xpath(
                '''div[@class="offer-item__content"]/
                div[@class="offer-item__title"]/
                h2[@class="offer-title"]/
                a[@class="offer-title__link"]/
                @href'''
            ).extract()[0]

            item['link'] = link

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

            item['location'] = ad.xpath(
                '''div[@class="offer-item__content"]/
                div[@class="offer-item__bottom-row "]/
                span[@class="offer-item__location"]/
                h4/
                em/
                text()'''
            ).extract()

            yield item

            '''yield scrapy.Request(
                link,
                self.parse_content,
                meta={'item': item}
            )'''

    def parse_content(self, response):
        item2 = response.meta['item']
        print('parse_content')
        yield item2

        '''item['brand'] = Selector(response).xpath(
            '//*[@id="parameters"]/ul[1]/li[2]/div/a/@title'
        )'''
