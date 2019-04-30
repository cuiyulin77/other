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
    publish_time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    media = scrapy.Field()
    create_time = scrapy.Field()
    # read_num = scrapy.Field()  # 阅读数量
    # comment_num = scrapy.Field()  # 评论数量
    # collection_num = scrapy.Field()  # 收藏数量
    # reprint_num = scrapy.Field()  # 转载数量
