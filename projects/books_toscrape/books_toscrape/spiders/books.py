"""CrawlSpider for the Books to Scrape catalogue.

Stable selectors (sandbox markup, safe to hard-code in the lessons):

    book card     //article[@class="product_pod"]
    title         .//h3/a/@title
                  The visible link text is truncated ("A Light in the ...").
                  The title attribute is the full title.
    price         .//p[@class="price_color"]/text()          e.g. £51.77
    availability  .//p[contains(@class, "availability")]/text()
                  Whitespace surrounds the words "In stock".
    rating        .//p[contains(@class, "star-rating")]/@class
                  e.g. "star-rating Three"
    detail url    .//h3/a/@href
                  Page 1 hrefs are relative to the site root
                  (catalogue/<slug>/index.html). Later pages are relative
                  to /catalogue/ (<slug>/index.html). response.urljoin
                  resolves both.
    next page     //li[@class="next"]/a
                  Page 1 -> catalogue/page-2.html
                  Page 2 -> page-3.html
                  There are 50 pages, 20 books each.

Do not override parse(). CrawlSpider.parse (via _parse) is what applies
these rules. Page 1 is handled in parse_start_url; later pages use the
rule callback. Both call parse_books so every page yields items.
"""

from books_toscrape.items import BookItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=('//li[@class="next"]/a',)),
            callback="parse_books",
            follow=True,
        ),
    )

    def parse_start_url(self, response, **kwargs):
        return self.parse_books(response)

    def parse_books(self, response):
        for book in response.xpath('//article[@class="product_pod"]'):
            loader = ItemLoader(item=BookItem(), selector=book, response=response)
            loader.add_xpath("title", ".//h3/a/@title")
            loader.add_xpath("price", './/p[@class="price_color"]/text()')
            loader.add_xpath(
                "availability",
                './/p[contains(@class, "availability")]/text()',
            )
            loader.add_xpath(
                "rating",
                './/p[contains(@class, "star-rating")]/@class',
            )
            href = book.xpath(".//h3/a/@href").get()
            if href:
                loader.add_value("url", response.urljoin(href))
            yield loader.load_item()
