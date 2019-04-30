# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WxSpiderItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    # media = scrapy.Field()  # 这里不加media，在插入数据库的时候直接指定,且仅指定es中的数据
    create_time = scrapy.Field()
    comm_num = scrapy.Field()  # 评论数量
    read_num = scrapy.Field()  # 阅读量
    fav_num = scrapy.Field()  # 点赞，喜欢数量
    env_num = scrapy.Field()  # 转发量
    user_name = scrapy.Field()
