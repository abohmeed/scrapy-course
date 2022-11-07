import scrapy
from wikipedia.items import WikipediaItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest


class SplashSpider(scrapy.Spider):
    name = 'splash'
    allowed_domains = ['www.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Web_scraping']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={
                'wait': 1
            })

    def parse(self, response):
        item = ItemLoader(item=WikipediaItem(),response=response,selector=response)
        item.add_xpath("title","//span[@class='mw-page-title-main']/text()")
        item.add_xpath("content","//div[@class='mw-parser-output']")
        yield item.load_item()
