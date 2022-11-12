# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join

class YahoofinanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=Join())
    change = scrapy.Field(output_processor=Join())
    timestamp = scrapy.Field(output_processor=Join())
