import schedule
import time
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from project.spiders.stand_virtual_spider import StandVirtualSpider
from project.spiders.custo_justo_spider import CustoJustoSpider
from project.spiders.olx_spider import OlxSpider
from scrapy.utils.project import get_project_settings


def run_spiders():
    print("Start one process at {time}.".format(time=time.time()))
    print('Crawl started...')
    start_time = time.time()

    settings = get_project_settings()

    # mySettings = {'ITEM_PIPELINES': {'project.pipelines.MongoDBPipeline': 300}}

    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(CustoJustoSpider)
    runner.crawl(StandVirtualSpider)
    runner.crawl(OlxSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    total_time = time.time() - start_time
    print('Crawl stoped. total time of crawling: {time}'.format(time=total_time))


def start_one_process():
    run_spiders()

def start_schedule():
    run_spiders()
    schedule.every().hour.do(run_spiders)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    def choose():
        choice = input(
            '''Are you sure you want to start the crawling process? : '''
        )
        if choice == 'y' or choice == 'yes':
            start_schedule()
        if choice == 'n' or choice == 'no':
            exit()
        if choice == 'dev' or choice == 'd':
            start_one_process()
        else:
            print('Invalid choice. Try again.')
            choose()
    choose()
