# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

# Books to Scrape star classes look like "star-rating Three".
_RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def strip_text(value):
    """Input processor. Drop leading and trailing whitespace."""
    return value.strip()


def clean_price(value):
    """Input processor. '£51.77' becomes '51.77'."""
    return value.replace("£", "").strip()


def rating_out(values):
    """Output processor. 'star-rating Three' becomes 3.

    Mirrors the early-course pattern of a custom output processor that
    turns raw extracted strings into one cleaned value.
    """
    for value in values:
        if not value or not value.strip():
            continue
        word = value.strip().split()[-1]
        return _RATING_WORDS.get(word, word)
    return None


class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(strip_text),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(strip_text, clean_price),
        output_processor=TakeFirst(),
    )
    availability = scrapy.Field(
        input_processor=MapCompose(strip_text),
        output_processor=TakeFirst(),
    )
    rating = scrapy.Field(
        output_processor=rating_out,
    )
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )
