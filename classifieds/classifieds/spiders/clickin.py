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
            # Get all the links from the start page that are contained inside the div with id of 'dashboard_block'
                "//div[@id='dashboard_block']")),
            callback="parse", follow=True
        ),
    )

    def parse(self, response):
        self.log(response.url)
        item = ItemLoader(item=ClassifiedsItem(),
                          response=response, selector=response)
        # The name is contained in h1 with class of 'clickin-post-title'
        item.add_xpath("name", ".//h1[@class='clickin-post-title']/text()")
        # The address, locality, landline, mobile, and price fields are all contained in  divs with 'clickin-post-blackbold' 
        # so we needed to find the sibling div with the appropriate label.
        # For example, the address div has a sibling div containing 'Address' value.
        item.add_xpath("address", "//div[div='Address']/div/p/text()")
        item.add_xpath(
            "locality", "//td[div='Locality ']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath("description", "//p[@class='clickin-desc-text']/text()")
        item.add_xpath(
            "landline", "//div[div='Landline']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath(
            "mobile", "//div[div='Mobile']/div[@class='clickin-post-blackbold']/text()")
        item.add_xpath(
            "price", "//td[div='Price']/div[@class='clickin-post-blackbold']/text()")
        yield item.load_item()
        # Pagination using the next page URL
        next_page = response.xpath('//a[@title="Next Page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
