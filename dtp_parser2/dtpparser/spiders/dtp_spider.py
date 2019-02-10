import scrapy
from scrapy.http.request import Request
from scrapy.http import FormRequest

import re
import json
from ast import literal_eval
import datetime
import urllib.parse as urlparse



def open_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


def dates_generator():
    now = datetime.datetime.now()
    ctr = datetime.datetime(2015, 1, 1)

    dates_set = set()

    while ctr <= now:
        ctr += datetime.timedelta(days=1)
        dates_set.add(datetime.datetime(ctr.year, ctr.month, 1).strftime('%m.%Y'))

    return list(dates_set)


class DtpSpider(scrapy.Spider):
    name = "dtp"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': "data/dtp.json"
    }

    def start_requests(self):

        regions = open_json('data/regions.json')

        for region in regions:
            for date in dates_generator():
                payload = dict()
                payload["data"] = '{"date":["MONTHS:' + date + '"],"ParReg":"' + region['parent_region_code'] + '","order":{"type":"1","fieldName":"dat"},"reg":"' + region['oktmo_code'] + '","ind":"1","st":"1","en":"10000"}'

                yield Request("http://stat.gibdd.ru/map/getDTPCardData", method="POST", meta=region, body=json.dumps(payload), headers={'Content-Type': 'application/json; charset=UTF-8'})

    def parse(self, response):
        export = json.loads(response.body_as_unicode())
        if export['data']:
            export = literal_eval(export['data'])

            for dtp in export['tab']:
                export_dtp = dict(dtp)
                export_dtp['area_name'] = response.meta['area_name']
                export_dtp['parent_region_name'] = response.meta['parent_region_name']
                export_dtp['parent_region_code'] = response.meta['parent_region_code']
                export_dtp['oktmo_code'] = response.meta['oktmo_code']
                yield export_dtp



