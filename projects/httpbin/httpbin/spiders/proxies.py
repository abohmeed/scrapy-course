import scrapy
import json


class UseragentSpider(scrapy.Spider):
    name = 'proxies'
    allowed_domains = ['httpbin.org']
    start_urls = ['https://httpbin.org/ip']

    def parse(self, response):
        payload = json.loads(response.body)
        yield (payload)
        yield scrapy.Request(self.start_urls[0], dont_filter=True)
