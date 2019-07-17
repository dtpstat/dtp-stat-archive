import scrapy
from scrapy.http.request import Request
from scrapy.http import FormRequest


import re
import json
from ast import literal_eval
import urllib.parse as urlparse

from parser.dtpparser.items import RegionItem


class RegionSpider(scrapy.Spider):
    name = "regions"

    start_urls = ['http://stat.gibdd.ru/']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': "data/regions.json"
    }

    def parse(self, response):

        # ищем скрипт с кодами ОКТМО регионов и выкачиваем их
        scripts = response.xpath('//script')

        for script in scripts:
            if script.extract() is not None and "downloadRegListData" in script.extract():
                string = script.extract()
                p = re.compile(r"downloadRegListData = (.*?);", re.MULTILINE)
                m = p.search(string)
                data = m.groups()[0]
                jdata = json.loads(data)
                for federal_district in jdata[0]["Nodes"]:
                    for region in federal_district["Nodes"]:
                        region_name = region['Text'].replace("г.", "").replace("гор.", "").strip()
                        region_data = {
                            "code": region['Value'],
                            "name": region_name
                        }
                        payload = {
                            "maptype": "1",
                            "region": region['Value'],
                            "pok": "1"
                        }
                        body = json.dumps(payload)
                        yield Request("http://stat.gibdd.ru/map/getMainMapData", method="POST",callback=self.parse_region, meta=region_data, body=body, headers={'Content-Type': 'application/json; charset=UTF-8'})

    def parse_region(self, response):
        export = json.loads(response.body_as_unicode())['metabase']
        export = json.loads(literal_eval(export)[0]['maps'])
        for area in export:
            Item = RegionItem()
            Item['area_name'] = area["name"].replace("г.", "").replace("гор.", "").replace("ГО", "").strip()
            Item['oktmo_code'] = area["id"]
            Item['parent_region_name'] = response.meta['name']
            Item['parent_region_code'] = response.meta['code']

            yield Item
