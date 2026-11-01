"""Starter spider for Scrapy Unleashed.

Run from the repository root, after installing requirements:

    python spider.py

Prints a JSON list of books from the first page of
https://books.toscrape.com/. Each object has title, price, and availability.
"""

import json

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess

# Stable selectors on the books.toscrape.com sandbox (they do not change):
#   book card:    //article[@class="product_pod"]
#   title:        .//h3/a/@title          (link text is truncated; @title is full)
#   price:        .//p[@class="price_color"]/text()
#   availability: .//p[contains(@class, "availability")]/text()
# The catalogue has 50 pages. This starter scrapes page 1 only.
# Pagination lives in projects/books_toscrape.


class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.xpath('//article[@class="product_pod"]'):
            availability = " ".join(
                part.strip()
                for part in book.xpath(
                    './/p[contains(@class, "availability")]/text()'
                ).getall()
                if part.strip()
            )
            # Yield the item. Scrapy only counts, exports, and pipelines items
            # that parse() yields. Appending to a class list and forgetting to
            # yield leaves that list empty under CrawlerProcess when nothing
            # was extracted, and `scrapy crawl` never sees the data.
            yield {
                "title": book.xpath(".//h3/a/@title").get(),
                "price": book.xpath('.//p[@class="price_color"]/text()').get(),
                "availability": availability,
            }


def _item_is_complete(item):
    return all(item.get(field) for field in ("title", "price", "availability"))


if __name__ == "__main__":
    scraped = []

    def collect_item(item, response, spider):
        scraped.append(dict(item))

    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
            "ROBOTSTXT_OBEY": True,
        }
    )
    process.crawl(BooksSpider)
    # Connect before start(): CrawlerProcess drops finished crawlers, so the
    # signal has to be attached while process.crawlers is still populated.
    for crawler in process.crawlers:
        crawler.signals.connect(collect_item, signal=signals.item_scraped)
    process.start()

    if not scraped or not all(_item_is_complete(item) for item in scraped):
        raise SystemExit(
            "No book data scraped from https://books.toscrape.com/. "
            "Expected a non-empty JSON list of title, price, and availability."
        )

    print(json.dumps(scraped, indent=4, ensure_ascii=False))
