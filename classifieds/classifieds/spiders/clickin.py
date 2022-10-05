import scrapy
from classifieds.items import ClassifiedsItem
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ClickinSpider(CrawlSpider):
    name = 'clickin'
    allowed_domains = ['click.in']
    start_urls = ['https://www.click.in/automobiles-ctgid150']
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=(
                "//div[@id='dashboard_block']")),
            callback="parse", follow=True
        ),
    )

    def parse(self, response):
        self.log(response.url)
        item = ItemLoader(item=ClassifiedsItem(),
                          response=response, selector=response)
        item.add_xpath("name", ".//h1[@class='clickin-post-title']/text()")
        item.add_xpath(
            "locality", "//td[div='Locality ']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath("address", "//div[div='Address']/div/p/text()")
        item.add_xpath("description", "//p[@class='clickin-desc-text']/text()")
        item.add_xpath(
            "landline", "//div[div='Landline']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath(
            "mobile", "//div[div='Mobile']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath(
            "price", "//td[div='Price']/div[@class='clickin-post-blackbold']/text()")
        yield item.load_item()
        next_page = response.xpath('//a[@title="Next Page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
