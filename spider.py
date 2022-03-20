import scrapy
from scrapy.crawler import CrawlerProcess
import json


class PythonListingSpider(scrapy.Spider):
    name = 'pythonlistingssspider'

    start_urls = ['https://www.arizonarealestate.com/maricopa/', ]
    found_listings = []

    def parse(self, response):
        gallery = response.xpath('//div[@class="si-listings-column"]')
        for listing in gallery:
            listing_details = dict()
            listing_details['name'] = listing.xpath(
                'div/a/div/div[@class="si-listing__title-main"]/text()').get()
            listing_details['description'] = listing.xpath(
                'div/a/div/div[@class="si-listing__title-main"]/text()').get()
            listing_details['price'] = listing.xpath(
                'div/div/a/div/span/text()').get()
            listing_details['agency'] = listing.xpath(
                'div/div/div[@class="si-listing__footer"]/div/text()').get()
            self.found_listings.append(listing_details)


if __name__ == "__main__":
    process = CrawlerProcess({'LOG_LEVEL': 'ERROR'})
    process.crawl(PythonListingSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    print(json.dumps(PythonListingSpider.found_listings, indent=4))
