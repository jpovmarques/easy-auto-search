import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from project.items import StandVirtualItem
from project.utils.regex_handler import (
    extract_beetwen_quotes,
    remove_spaces_and_paragraph
)


class StandVirtualSpider(Spider):
    name = "standvirtual"

    allowed_domains = [
        "https://www.standvirtual.com",
        "www.standvirtual.com"
    ]

    def start_requests(self):
        url = (
            'https://www.standvirtual.com/'
            'carros/{brand}/?search%5Bnew_used%5D=on'
            .format(brand=self.brand)
        )
        yield scrapy.Request(url, self.parse)


    def parse(self, response):
        '''Extract ad preview's content into item object'''
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
            ).extract()[0].rstrip()

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

            if picture is not None:
                match = extract_beetwen_quotes(picture)
                if match is not None:
                    item['picture'] = match
            try:
                item['location'] = ad.xpath(
                    '''div[@class="offer-item__content"]/
                    div[@class="offer-item__bottom-row "]/
                    span[@class="offer-item__location"]/
                    h4/
                    em/
                    text()'''
                ).extract()[0]
            except IndexError:
                    item['location'] = None

            # yield scrapy.Request(
            #     link,
            #     self.parse_content,
            #     meta={'item': item}
            # )

            yield item

    def parse_content(self, response):
        '''Extract ad's full content into item object'''
        item = response.meta['item']

        item['brand'] = Selector(response).xpath(
            '//*[@id="parameters"]/ul[1]/li[2]/div/a/@title'
        ).extract()[0]

        item['model'] = Selector(response).xpath(
            '//*[@id="parameters"]/ul[1]/li[3]/div/a/@title'
        ).extract()[0]

        try:
            item['serie'] = Selector(response).xpath(
                '//*[@id="parameters"]/ul[1]/li[4]/div/a/@title'
            ).extract()[0]
        except IndexError:
            item['version'] = None

        try:
            version = Selector(response).xpath(
                '//*[@id="parameters"]/ul[1]/li[5]/div/text()'
            ).extract()[0]
            item['version'] = remove_spaces_and_paragraph(version)
        except IndexError:
            item['version'] = None

        kms = Selector(response).xpath(
            '//*[@id="parameters"]/ul[1]/li[9]/div/text()'
        ).extract()[0]
        item['kms'] = remove_spaces_and_paragraph(kms)

        try:
            capacity = Selector(response).xpath(
                '//*[@id="parameters"]/ul[1]/li[11]/div/text()'
            ).extract()[0]
        except IndexError:
            try:
                capacity = Selector(response).xpath(
                    '//*[@id="parameters"]/ul[2]/li[2]/div'
                ).extract()[0]
            except IndexError:
                capacity = None

        if capacity is not None and not '':
            item['capacity'] = remove_spaces_and_paragraph(capacity)

        yield item
