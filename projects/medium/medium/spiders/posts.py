import scrapy
from selenium import webdriver
import time
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from medium.items import MediumItem


class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['medium.com']
    start_urls = ['https://medium.com/']

    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_result)

    def parse_result(self, r):
        options = webdriver.FirefoxOptions()
        options.headless = True
        desired_capabilities = options.capabilities
        driver = webdriver.Firefox(
            desired_capabilities=desired_capabilities, options=options)
        driver.get(self.start_urls[0])
        driver.implicitly_wait(5)
        i = 1
        num_scrolls = 10
        while i <= num_scrolls:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            response = driver.page_source
            selector = Selector(text=driver.page_source)
            containers = selector.xpath("//section//div[@class='ae cx']")
            for c in containers:
                item = ItemLoader(item=MediumItem(),
                                  response=response, selector=c)
                item.add_xpath("title", ".//h2/text()")
                item.add_xpath("excerpt", ".//h3/text()")
                item.add_xpath("link", ".//a[h2]/@href")
                yield item.load_item()
            i = i + 1
        driver.quit()
