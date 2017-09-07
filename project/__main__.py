from scrapy.crawler import CrawlerProcess
from project.spiders.stand_virtual_spider import StandVirtualSpider
from project.utils.network_handler import NetworkUtils


def main():
    input_brand = input('Brand:')
    process = CrawlerProcess(NetworkUtils.get_user_agent())
    process.crawl(StandVirtualSpider, brand=input_brand)
    process.start()

if __name__ == "__main__":
    main()
