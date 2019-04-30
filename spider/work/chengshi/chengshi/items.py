# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengshiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 共12个字段
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    media = scrapy.Field()
    # 192.168.3.15的classid:旅游(165),人物(164),养生(166),美食(167),天下(170)
    classid = scrapy.Field()  # 所需要存放的栏目的id
    keyid = scrapy.Field()  # 关键字
    writer = scrapy.Field()  # 作者
    newstime = scrapy.Field()  # 字符串格式的时间转化为10位的时间戳
    titlepic = scrapy.Field()  # 标题图片 应取新闻第一张图片,否则就为' '