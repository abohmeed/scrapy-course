# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector


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


class MySQLPipeline:
    def __init__(self, mysql_host, mysql_username, mysql_password, mysql_database):
        self.mysql_host = mysql_host
        self.mysql_username = mysql_username
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_username=crawler.settings.get('MYSQL_USERNAME'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_database=crawler.settings.get('MYSQL_DATABASE')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.mysql_host,
            user=self.mysql_username,
            password=self.mysql_password,
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"""CREATE DATABASE IF NOT EXISTS {self.mysql_database}""")
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.mysql_database}.classifieds(
                id int NOT NULL auto_increment,
                title TEXT,
                locality TEXT,
                address TEXT,
                landline TEXT,
                mobile TEXT,
                price FLOAT,
                PRIMARY KEY (id)
            )"""
                         )

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cur.execute(f"""INSERT INTO {self.mysql_database}.classifieds (title,locality,address,landline,mobile,price) VALUES (%s,%s,%s,%s,%s,%s)""",
                         (adapter.get("title", ""), adapter.get("locality", ""), adapter.get("address", ""), adapter.get("landline", ""),
                          adapter.get("mobile", ""), adapter.get("price", 0.0))
                         )
        self.conn.commit()
        return item
