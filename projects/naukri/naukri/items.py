# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from datetime import date
from scrapy.loader.processors import Join, MapCompose


def date_out(d):
    d = d/1000  # Get rid of the millseconds
    return str(date.fromtimestamp(d))


class NaukriItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(output_processor=Join())
    company = scrapy.Field(output_processor=Join())
    description = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processror=Join())
    location = scrapy.Field(output_processor=Join())
    date = scrapy.Field(output_processor=MapCompose(date_out))
