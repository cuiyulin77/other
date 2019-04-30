# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    blogger_name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    media = scrapy.Field()
    create_time = scrapy.Field()
