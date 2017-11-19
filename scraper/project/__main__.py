import schedule
import time
from scrapy.crawler import CrawlerProcess
from project.spiders.stand_virtual_spider import StandVirtualSpider
from scrapy.utils.project import get_project_settings


def run_standvirtual_spider():
    print("Starting a job...")
    print('Crawl started...')
    start_time = time.time()
    process = CrawlerProcess(get_project_settings())
    process.crawl(StandVirtualSpider)
    process.start()
    total_time = time.time() - start_time
    print('Crawl stoped. total time of crawling: {time}'.format(time=total_time))

def start_one_process():
    print("Start one process.")
    run_standvirtual_spider()

def start_schedule():
    run_standvirtual_spider()
    # schedule.every().hour.do(run_standvirtual_spider)
    schedule.every(30).minutes.do(run_standvirtual_spider)

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
