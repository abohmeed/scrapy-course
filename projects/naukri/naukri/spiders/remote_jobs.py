import scrapy
import json
from naukri.items import NaukriItem
from scrapy.loader import ItemLoader
from math import ceil


class RemoteJobsSpider(scrapy.Spider):
    name = 'remote_jobs'
    allowed_domains = ['naukri.com']
    start_urls = ['https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv'
                  '&keyword=remote&pageNo=2&seoKey=remote-jobs&src=discovery_trendingWdgt_homepage_srch&latLong=']
    page = 1

    def parse(self, response):
        payload = json.loads(response.body)
        total = payload['noOfJobs']
        page_count = ceil(total / 20)
        for j in payload['jobDetails']:
            i = ItemLoader(item=NaukriItem())
            i.add_value('title', j['title'])
            i.add_value('company', j['companyName'])
            i.add_value('description', j['jobDescription'])
            i.add_value(
                'location', (x['label'] for x in j['placeholders'] if x['type'] == 'location'))
            i.add_value('date', j['createdDate'])
            yield i.load_item()
        while self.page <= page_count:
            self.page = self.page + 1
            base_url = 'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType' \
                       '=adv&keyword=remote&pageNo={' \
                       '}&seoKey=remote-jobs&src=discovery_trendingWdgt_homepage_srch&latLong='.format(self.page)
            yield response.follow(base_url, callback=self.parse)
