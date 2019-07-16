# -*- coding: utf-8 -*-
import psycopg2
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from parser.extra import open_json
from parser.extra import save_json

hostname = 'localhost'
username = 'dtpmap'
password = 'dtpmap'
database = 'dtpmap'

class RegionPipeline(object):

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):

        sql_query = """
            INSERT INTO dtpmapapp_region
              (name, oktmo_code, level)
            VALUES
              (NULL , %s, %s)
            ON CONFLICT (code) DO UPDATE
            SET name_en = %s;
        """

        name = region[0],
        oktmo_code = region[1]['code'],
        level = 1,
        alias = slugify(region[0]),
        status = False

        self.cur.execute(sql_query, (item['name'], item['code'], item['name']))

        self.connection.commit()
        return item

"""
class DTPPipeline(object):
    def open_spider(self, spider):
        self.data = open_json("data/dtp.json")

    def process_item(self, item, spider):
        self.data.append(item)

    def close_spider(self, spider):
        save_json(self.data, "data/dtp.json")
"""