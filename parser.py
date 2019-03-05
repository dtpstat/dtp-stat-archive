#!/usr/bin/env python

import sys
import os
import warnings
import locale
import csv

import django
sys.path.append(os.path.join(os.path.dirname(__file__), '../dtpmap/dtpmap'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtpmap.settings")
django.setup()

try:
    locale.setlocale(locale.LC_TIME, "ru_RU")
except locale.Error:
    # right locale for GNU/Linux
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF8")

warnings.filterwarnings('ignore')

from dtpmapapp import models
from django.shortcuts import get_object_or_404


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from dtp_parser2.dtpparser.spiders.region_spider import RegionSpider
from dtp_parser2.dtpparser.spiders.dtp_spider import DtpSpider
from dtp_parser2 import update_dtp

from dtp_parser2 import geocoder


def open_csv(link):
    with open(link, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
        return data


def get_tech_data():
    for participant_type in open_csv("data/participant_types.csv"):
        participant_type_item, created = models.MVCParticipantType.objects.get_or_create(
            name=participant_type[0]
        )
        if created:
            participant_type_item.label = participant_type[1]

        participant_type_item.value = True if participant_type[2] == "true" else False
        participant_type_item.save()


def download_regions():
    print("lol")
    if os.path.exists("data/regions.json"):
        os.remove("data/regions.json")

    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'dtp_parser2.dtpparser.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    process = CrawlerProcess(settings)

    process.crawl(RegionSpider)
    process.start()


def get_regions_from_file():
    regions_data = open_csv("data/regions.csv")

    for region in regions_data:
        if region[7]:
            parent_region = get_object_or_404(models.Region, oktmo_code=region[8],level=1)
            region_item, created = models.Region.objects.get_or_create(
                oktmo_code=region[1],
                level=region[3],
                parent_region_id=parent_region.id
            )
        else:
            region_item, created = models.Region.objects.get_or_create(
                oktmo_code=region[1],
                level=region[3]
            )

        if created:
            region_item.name = region[0]

        region_item.alias = region[2]
        region_item.latitude = region[5]
        region_item.longitude = region[6]
        region_item.status = True if region[4] == "TRUE" else False

        region_item.save()


def download_dtp():
    if os.path.exists("data/dtp.json"):
        os.remove("data/dtp.json")
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'dtp_parser2.dtpparser.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    process = CrawlerProcess(settings)

    process.crawl(DtpSpider)
    process.start()


def get_dtp():
    update_dtp.main()


def geocode_dtp():
    geocoder.new_geocoder()

def load(data):
    if len(data) > 0:
        for item in data:
            if item == "tech_data":
                get_tech_data()
            elif item == "download_regions":
                download_regions()
            elif item == "get_regions":
                get_regions_from_file()
            elif item == "download_dtp":
                download_dtp()
            elif item == "get_dtp":
                get_dtp()
            elif item == "geocode_dtp":
                geocode_dtp()
    else:
        get_tech_data()
        #download_regions()
        get_regions_from_file()
        #download_dtp()
        get_dtp()
        #geocode_dtp()

def main(args):
    load(args[1:])


if __name__ == "__main__":
    main(sys.argv)

