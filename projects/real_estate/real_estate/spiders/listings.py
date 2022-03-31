import scrapy
from real_estate.items import RealEstateItem


class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['arizonarealestate.com']
    start_urls = [
        'https://www.arizonarealestate.com/maricopa/',
        'https://www.arizonarealestate.com/goodyear/',
        'https://www.arizonarealestate.com/tempe/'
    ]

    def parse(self, response):
        gallery = response.xpath('//div[@class="si-listings-column"]')
        for listing in gallery:
            item = RealEstateItem()
            item['name'] = listing.xpath(
                './/div[@class="si-listing__title-main"]/text()').get()
            item['description'] = listing.xpath(
                './/div[@class="si-listing__title-description"]/text()').get()
            item['price'] = listing.xpath(
                './/div[@class="si-listing__photo-price"]/span/text()').get()
            item['agency'] = listing.xpath(
                './/div[@class="si-listing__footer"]/div/text()').get()
            yield item
