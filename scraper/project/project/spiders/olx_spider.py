import re
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from ..items import CarItem


class OlxSpider(Spider):
    name = "olx"
    allowed_domains = [
        'https://www.olx.pt',
        'www.olx.pt'
    ]

    def start_requests(self):
        url = (
            "https://www.olx.pt/carros-motos-e-barcos/carros/"
        )
        self.source_name = 'olx'
        yield scrapy.Request(url, self.parse_sitemap)

    def parse_sitemap(self, response):
        # page_number = int(Selector(response).xpath(
        # '''//*[@id="body-container"]/div[3]/div/div[4]/span[16]/a/span/text()'''
        # ).extract_first())
        for page in range(501):
            url = 'https://www.olx.pt/carros-motos-e-barcos/carros/?search%5Bdescription%5D=1&page={page}'.format(page=page)

            yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        """
        Parse ad preview's data into item object and follow all the ad content links
        """
        ad_previews = Selector(response).xpath( # TODO problem here
            '''//*[@id="offers_table"]/tbody/tr[@class="wrap"]'''
        )
        for ad in ad_previews:
            item = CarItem()
            item['source'] = self.source_name

            basePath = 'td[@class="offer "]/table/tbody/'

            link = ad.xpath(
                '''{}tr/td[@rowspan="2"]/a/@href'''.format(basePath)
            ).extract_first()
            item['link'] = link

            picture = ad.xpath(
                '''{}tr/td[@rowspan="2"]/a/img/@src'''.format(basePath)
            ).extract_first()
            item['picture'] = picture

            location = ad.xpath(
                '''{}tr/td[@valign="bottom"]/div[@class="space rel"]/p/small/span/text()'''.format(basePath)
            ).extract_first()
            if location: location = location.strip()
            item['location'] = location

            price = ad.xpath(
                '''{}tr/td[@class="wwnormal tright td-price"]/div/p[@class="price"]/strong/text()'''.format(basePath)
            ).extract_first()
            if price: price = int(price.replace('€', '').replace('Troca', '0').replace('.', '').strip())
            item['price'] = price

            title = ad.xpath(
                '''{}tr/td[@valign="top"]/div[@class="space rel"]/h3/a/strong/text()'''.format(basePath)
            ).extract_first()
            item['title'] = title

            brand = ad.xpath(
                '''{}tr/td[@valign="top"]/div[@class="space rel"]/p/small/text()'''.format(basePath)
            ).extract_first()
            if brand: brand = brand.replace('Carros »', '').strip()
            item['brand'] = brand

            print('----->', item)

            if item['link']:
                yield scrapy.Request(
                    link,
                    callback=self.parse_content,
                    meta={'item': item},
                    dont_filter=True
                )

    def parse_content(self, response):
        item = response.meta['item']

        ad_table_content = Selector(response).xpath(
            '''//*[@id="offerdescription"]/div[3]/table'''
        )

        for ad_col_content in ad_table_content:
            left_list = ad_col_content.xpath('''tr/td/table/tr/th/text()''').extract()
            right_raw_link = [x.strip() for x in ad_col_content.xpath('''tr/td/table/tr/td[@class="value"]/strong/a/text()''').extract()]
            right_raw_no_link = [x.strip() for x in ad_col_content.xpath('''tr/td/table/tr/td[@class="value"]/strong/text()''').extract()]

            new_right_raw_no_link = []
            for x in right_raw_no_link:
                x = x.strip()
                if x is not '':
                    new_right_raw_no_link.append(x)
            right_list = right_raw_link[0:3] + new_right_raw_no_link + right_raw_link[3:10]

        for tuple_item in zip(left_list, right_list):
            if tuple_item[0] == 'Modelo': item['model'] = tuple_item[1]
            if tuple_item[0] == 'Ano': item['year'] = tuple_item[1]
            if tuple_item[0] == 'Quilómetros': item['kms'] = tuple_item[1]
            if tuple_item[0] == 'Combustível': item['gas_type'] = tuple_item[1]

        yield item
