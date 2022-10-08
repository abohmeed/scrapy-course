# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlite3 import adapt
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ClassifiedsRemoveDuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] in self.titles_seen:
            raise DropItem(f"Duplicate ad detected: {item}")
        else:
            self.titles_seen.add(adapter["title"])
        return item


class ClassifiedsRemoveNoPhonesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get("landline") and not adapter.get("mobile"):
            raise DropItem(f"Ad with no contact info detected: {item}")
        else:
            return item
