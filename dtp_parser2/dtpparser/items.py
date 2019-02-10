# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class RegionItem(Item):
    area_name = Field()
    oktmo_code = Field()
    parent_region_name = Field()
    parent_region_code = Field()

    pass

