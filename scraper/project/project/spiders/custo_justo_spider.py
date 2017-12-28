import re
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from ..items import CarItem


class CustoJustoSpider(Spider):
    name = "custojusto"
    allowed_domains = [
        'http://www.custojusto.pt',
        'www.custojusto.pt'
    ]

    def start_requests(self):
        url = (
            "http://www.custojusto.pt/portugal/carros-usados"
        )
        self.source_name = 'custojusto'
        yield scrapy.Request(url, self.parse_sitemap)

    def parse_sitemap(self, response):
        last_page_url = Selector(response).xpath(
            ('''///html/body/div[5]/div/div/div[3]/div/div/div/ul[2]/li/a''')
        ).extract_first()
        try:
            last_page_number = int(re.fullmatch(r"(.+)o=([\d]+)&(.+)", last_page_url).group(2))
            for page in range(0, last_page_number + 1):
                url = 'http://www.custojusto.pt/portugal/carros-usados?o={page}&st=a'.format(page=page)
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    dont_filter=True
                )
        except Exception as e:
            return None

    def parse(self, response):
        """
        Parse ad preview's data into item object and follow all the ad content links
        """

        ad_previews = Selector(response).xpath(
            '//div[@id="dalist"]/a'
        )
        for ad in ad_previews:
            item = CarItem()
            item['source'] = self.source_name

            link = ad.xpath(
                '''@href'''
            ).extract_first()
            item['link'] = link

            picture_path_point = ('''div[@class="row results"]/
            div[@class="col-md-2 col-xs-4 no-padding imglist"]/
            img''')
            picture = (
                ad.xpath(picture_path_point + '/@data-src') or
                ad.xpath(picture_path_point + '/@src')
            ).extract_first()
            item['picture'] = picture

            title = ad.xpath(
                ('''div[@class="row results"]/
                div[@class="col-md-10 col-xs-8 no-padding-right norelative"]/
                h2/
                text()''')
            ).extract_first().strip()
            item['title'] = title

            location = ad.xpath(
                ('''div[@class="row results"]/
                div[@class="col-md-10 col-xs-8 no-padding-right norelative"]/
                div[@class="col-md-12 col-sm-12 col-xs-6 pull-left no-padding norelative"]/
                span[@class="hidden-xs"]/
                text()''')
            ).extract_first().strip()

            item['location'] = location

            price = ad.xpath(
                ('''div[@class="row results"]/
                div[@class="col-md-10 col-xs-8 no-padding-right norelative"]/
                h5/
                text()''')
            ).extract_first().strip().replace('€', '').replace(' ', '')
            item['price'] = price

            request = scrapy.Request(
                link,
                callback=self.parse_content,
                dont_filter=True
            )

            request.meta['item'] = item
            yield request

    def parse_content(self, response):
        """Parse ad's full content into item object"""
        item = response.meta['item']

        ad_content = Selector(response).xpath(
            ('''//html/body/
            div[@class="container"]/
            div[@class="row"]/
            div[@class="col-md-8"]/
            div[@class="row"]/
            div[@class="col-sm-5 col-sm-push-7 no-padding"]/
            ul[@class="list-group gbody"]/
            li''')
        )

        for content in ad_content:
            left_title_list = content.xpath(
                ('''text()''')
            ).extract()
            parsed_left_title_list = [i.strip() for i in left_title_list if i.strip()]
            parsed_left_title = parsed_left_title_list[0]

            right = content.xpath(
                ('''span[@class="badge value"]/
                text()''')
            ).extract_first()

            if parsed_left_title == 'Ano do modelo': item['year'] = right
            if parsed_left_title == 'Quilómetros': item['kms'] = right
            if parsed_left_title == 'Combustível': item['gas_type'] = right
            if parsed_left_title == 'Fabricante': item['brand'] = right
            if parsed_left_title == 'Modelo': item['model'] = right

        yield item
