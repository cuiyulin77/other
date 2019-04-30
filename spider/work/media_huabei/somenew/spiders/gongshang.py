# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 新浪内蒙古爬虫 首页:
# =============================================================================


class XinlangliaoningSpider(scrapy.Spider):
    name = 'gongshang'
    allowed_domains = ['huijuyun.com']
    start_urls = ['https://huijuyun.com/qiye?key=%E6%B7%B1%E5%9C%B3%E5%85%AC%E5%8F%B8']

    def parse(self, response):
        print(response.url)


