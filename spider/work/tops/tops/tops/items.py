# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    top_type = scrapy.Field()
    top_title = scrapy.Field()
    url = scrapy.Field()
    hot_value = scrapy.Field()
    media = scrapy.Field()
    summary = scrapy.Field()
    top_num = scrapy.Field()
