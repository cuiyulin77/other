# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 共12个字段
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    media = scrapy.Field()
    create_time = scrapy.Field()
    comm_num = scrapy.Field()  # 评论数量
    read_num = scrapy.Field()  # 阅读量
    fav_num = scrapy.Field()  # 点赞，喜欢数量
    env_num = scrapy.Field()  # 转发量
    media_type = scrapy.Field()  # 媒体类型
    come_from = scrapy.Field()  # 信息来源
    addr_province = scrapy.Field()  # 媒体所在省
    addr_city = scrapy.Field()  # 媒体所在市
