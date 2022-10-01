import scrapy


class MyimagesSpider(scrapy.Spider):
    name = 'myimages'
    allowed_domains = ['freeimages.com']
    start_urls = ['http://freeimages.com/']

    def parse(self, response):
        pass
