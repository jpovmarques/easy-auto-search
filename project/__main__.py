from scrapy.crawler import CrawlerProcess
from project.spiders.stand_virtual_spider import StandVirtualSpider
from project.utils.network import NetworkUtils


def main():
    lixo = NetworkUtils.choose_user_agent()
    print(lixo)
    process = CrawlerProcess(lixo)
    process.crawl(StandVirtualSpider)
    process.start()


if __name__ == "__main__":
    main()
