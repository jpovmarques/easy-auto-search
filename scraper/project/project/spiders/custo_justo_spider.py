import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from ..items import CarItem


class CustoJustoSpider(Spider):
    name = "custojusto"
    allowed_domains = ["*"]
    URL = None

    def start_requests(self):
        url = (
            "http://www.custojusto.pt/portugal/carros-usados"
        )
        self.URL = url
        yield scrapy.Request(url, self.parse)

    # def parse_sitemap(self, response):
    #     page_number_list = Selector(response).xpath(
    #         ('''//*[@id="body-container"]/
    #         div/div/ul/li/a/
    #         span[@class="page"]/
    #         text()''')
    #     ).extract()
    #
    #     for page_number in page_number_list:
    #         original_number = page_number
    #         page_number = RegexHandler.get_number_value(page_number)
    #         if not page_number:
    #             page_number_list.remove(original_number)
    #
    #     for number in range(1, int(page_number_list[-1]) + 1):
    #         url = self.URL + '?page={number}'.format(number=number)
    #         yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """
        Parse ad preview's data into item object and follow all the ad content links
        """
        ad_previews = Selector(response).xpath(
            '//div[@id="dalist"]/a'
        )
        for ad in ad_previews:
            item = CarItem()

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

        print('item', item)
