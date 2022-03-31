# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from ntpath import join
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import json


def description_in(d):
    return d.strip()

def description_out(d):
    o = [0,3,1,4,2,5]
    d = [d[i] for i in o]
    it = iter(d)
    # return json.dumps(dict(zip(it,it)))
    return dict(zip(it,it))


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(description_in),
        # output_processor=Join()
        output_processor=description_out
    )
    price = scrapy.Field()
    agency = scrapy.Field()
