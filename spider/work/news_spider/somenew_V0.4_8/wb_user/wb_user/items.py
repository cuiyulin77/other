# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WbUserItem(scrapy.Item):
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    user_url = scrapy.Field()
    fans = scrapy.Field()
    get_time = scrapy.Field()
    followers = scrapy.Field()
    summary = scrapy.Field()






