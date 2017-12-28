import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from ..items import CarItem
from ..utils.regex_handler import RegexHandler


class StandVirtualSpider(Spider):
    name = "standvirtual"
    allowed_domains = [
        "https://www.standvirtual.com",
        "www.standvirtual.com"
    ]

    def start_requests(self):
        url = (
            "https://www.standvirtual.com/carros/"
        )
        self.source_name = 'standvirtual'
        yield scrapy.Request(url, self.parse_sitemap)

    def parse_sitemap(self, response):
        page_number_list = Selector(response).xpath(
            ('''//*[@id="body-container"]/
            div/div/ul/li/a/
            span[@class="page"]/
            text()''')
        ).extract()

        for page_number in page_number_list:
            original_number = page_number
            page_number = RegexHandler.get_number_value(page_number)
            if not page_number:
                page_number_list.remove(original_number)

        for number in range(1, int(page_number_list[-1]) + 1):
            url = self.URL + '?page={number}'.format(number=number)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """
        Parse ad preview's data into item object and follow all the ad content links
        """
        ad_previews = Selector(response).xpath(
            '//div[@class="offers list"]/article'
        )
        for ad in ad_previews:
            item = CarItem()
            item['source'] = self.source_name

            gas_type = ad.xpath(
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
            ).extract_first().replace(' cv', "")
            if power:
                item['power'] = int(power)

            year = ad.xpath(
                ('''div[@class="offer-item__content"]/
                ul[@class="offer-item__params"]/
                li[@data-code="first_registration_year"]/
                span/
                text()''')
            ).extract_first()
            if year:
                item['year'] = int(year.strip().replace(" ", ""))

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
                item['price'] = int(price.strip().replace(" ", ""))

            picture = ad.xpath(
                ('''div[@class="offer-item__photo "]/
                a[@class="offer-item__photo-link"]/
                @style''')
            ).extract_first()
            if picture:
                match = RegexHandler.extract_beetwen_quotes(picture)
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

    def parse_content(self, response):
        """
        Parse ad's full content into item object
        """
        item = response.meta['item']

        ad_contents_left_column = Selector(response).xpath(
            '//*[@id="parameters"]/ul[1]'
        )
        ad_contents_right_column = Selector(response).xpath(
            '//*[@id="parameters"]/ul[2]'
        )
        ad_contents = ad_contents_left_column + ad_contents_right_column

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
            content_list_link_value = content_column.xpath(
                ('''li[@class="offer-params__item"]/
                div[@class="offer-params__value"]/
                a[@class="offer-params__link"]/
                @title''')
            ).extract()

            content_list_all_values = content_list_link_value + content_list_value

            for label, value in zip(content_list_label, content_list_all_values):
                if label == 'Marca' and value:
                    item['brand'] = value
                if label == 'Modelo' and value:
                    item['model'] = value

            for value in content_list_all_values:
                capacity_match = RegexHandler.get_capacity_value(value)
                if capacity_match:
                    item['capacity'] = int(capacity_match.replace(" cm3", "").replace(" ", ""))

                kms_match = RegexHandler.get_kms_value(value)
                if kms_match:
                    item['kms'] = int(kms_match.replace(" km", "").replace(" ", ""))

        yield item
