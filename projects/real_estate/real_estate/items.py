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
    labels = d[0:3]
    values = d[3:]
    output = {
        labels[0]: values[0],
        labels[1]: " ".join(values[1:-1]),
        labels[2]: values[-1]
    }
    return output


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(description_in),
        output_processor=description_out
    )
    price = scrapy.Field()
    agency = scrapy.Field()
