import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from project.items import StandVirtualItem
from project.utils.regex_handler import (
    _extract_beetwen_quotes,
    _remove_spaces_and_paragraph_from_list
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
        """Parse ad preview's data into item object"""
        ad_previews = Selector(response).xpath(
            '//div[@class="offers list"]/article'
        )
        for ad in ad_previews:
            item = StandVirtualItem()

            gas_type= ad.xpath(
                ('''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="fuel_type"]/
                span/
                text()''')
            ).extract_first()
            if gas_type:
                item['gas_type'] = gas_type

            power = ad.xpath(
                ('''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="power"]/
                span/
                text()''')
            ).extract_first()
            if power:
                item['power'] = power

            year = ad.xpath(
                ('''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="first_registration_year"]/
                span/
                text()''')
            ).extract_first()
            if year:
                item['year'] = year.rstrip()

            link = ad.xpath(
                ('''div[@class="offer-item__content"]/
                div[@class="offer-item__title"]/
                h2[@class="offer-title"]/
                a[@class="offer-title__link"]/
                @href''')
            ).extract_first()
            if link:
                item['link'] = link   

            title = ad.xpath(
                ('''div[@class="offer-item__content"]/
                div[@class="offer-item__title"]/
                h2[@class="offer-title"]/
                a[@class="offer-title__link"]/
                @title''')
            ).extract_first()
            if title:
                item['title'] = title

            price = ad.xpath(
                ('''div[@class="offer-item__content"]/
                div[@class="offer-item__price"]/
                div[@class="offer-price"]/
                span[@class="offer-price__number"]/
                text()''')
            ).extract_first()
            if price:
                item['price'] = price.rstrip()

            picture = ad.xpath(
                ('''div[@class="offer-item__photo "]/
                a[@class="offer-item__photo-link"]/
                @style''')
            ).extract_first()
            if picture:
                match = _extract_beetwen_quotes(picture)
                if match:
                    item['picture'] = match
            
            location = ad.xpath(
                ('''div[@class="offer-item__content"]/
                div[@class="offer-item__bottom-row "]/
                span[@class="offer-item__location"]/
                h4/
                em/
                text()''')
            ).extract_first()
            if location:
                item['location'] = location

            yield scrapy.Request(
                link,
                self.parse_content,
                meta={'item': item}
            )

            yield item

    def parse_content(self, response):
        """Parse ad's full content into item object"""
        item = response.meta['item']

        ad_contents = Selector(response).xpath(
            '//ul[@class="offer-params__list"]'
        )

        i = {}
        count_value = 0
        count_link = 0
        for content_column in ad_contents:
            content_list_label = content_column.xpath(
            ('''li[@class="offer-params__item"]/
                span[@class="offer-params__label"]/
                text()''')
            ).extract()
            content_list_value = content_column.xpath(
                ('''li[@class="offer-params__item"]/
                div[@class="offer-params__value"]/
                text()''')
            ).extract()
            content_list_link_value =content_column.xpath(
                ('''li[@class="offer-params__item"]/
                div[@class="offer-params__value"]/
                a[@class="offer-params__link"]/
                @title''')
            ).extract()

            for label in content_list_label:
                if label:
                    print({'label': label})
                    value = content_list_link_value[count_value]
                    link_value = content_list_value[count_value]
                    print({'value': value})
                    print({'link_value': link_value})                    
                    if value is not None and value.find('\n', 1, 2) != -1:
                        i[label] = value
                    elif link_value is not None and link_value.find('\n', 1, 2) != -1:
                        i[label] = link_value
                    count_value = count_value + 1

        print({'dict': i})
        yield item
