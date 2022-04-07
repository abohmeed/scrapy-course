import scrapy
from scrapy import Request


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        return [
            Request(
                "http://quotes.toscrape.com/login",
                callback=self.parse_login
            )
        ]

    def parse_login(self, response):
        ret = scrapy.FormRequest.from_response(response, formdata={
            "username": "ahmed",
            "password": "mypassword"
        })
        self.log("Sent:" + str(ret.body))
        return ret

    def parse(self, response):
        pass
