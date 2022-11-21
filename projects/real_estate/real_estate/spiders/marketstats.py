import scrapy
from real_estate.items import RealEstateItem
from scrapy.loader import ItemLoader
from datetime import datetime


class MarketstatsSpider(scrapy.Spider):
    name = 'marketstats'
    allowed_domains = ['arizonarealestate.com']
    start_urls = ['https://www.arizonarealestate.com/market-statistics/']

    def parse(self, response):
        containers = response.xpath("//div[@class='si-market-stat__box']")
        for c in containers:
            item = ItemLoader(item=RealEstateItem(),
                              response=response, selector=c)
            item.add_xpath(
                "county", ".//div[@class='si-market-stat__title']/text()")
            item.add_xpath("median_list_price",
                           ".//div[@class='si-market-stat__top']//div[3]/div[@class='si-market-stat__top-value']/text()")
            item.add_value("timestamp", str(datetime.now().timestamp()))
            yield item.load_item()
