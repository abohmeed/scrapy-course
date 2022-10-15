# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import boto3
import json
import hashlib


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


class UploadToS3Pipeline:
    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bucket=crawler.settings.get("S3_BUCKET")
        )

    def process_item(self, item, spider):
        s3_client = boto3.client('s3')
        item_bytes = json.dumps(ItemAdapter(item).asdict())
        item_key = hashlib.md5(item_bytes.encode()).hexdigest()
        s3_client.put_object(
            Body=item_bytes,
            Bucket=self.bucket,
            Key= item_key + ".json"
        )
        return item
