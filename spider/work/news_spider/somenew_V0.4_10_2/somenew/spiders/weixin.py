# -*- coding: utf-8 -*-

import scrapy
import re
import json
from somenew.items import SomenewItem
import pymysql
from w3lib.html import remove_tags
import datetime
import html
import hashlib
from urllib.parse import urlencode

class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['sogou.com']
    url_list = []
    # 连接云服务器mysql
    conn = pymysql.connect(host='47.92.166.26', port=3306, user='root', password='admin8152', database='xuanyuqing',
                           charset='utf8')
    cs1 = conn.cursor()
    cs1.execute('select  title from company_popular_feelings')
    result = cs1.fetchall()
    for res in result:
        # print(res)
        url = "http://weixin.sogou.com/weixin?type=2&s_from=input&query={keyword}&ie=utf8".format(keyword=res[0])
        url_list.append(url)
    url_list = list(set(url_list))
    start_urls = url_list

    def parse(self, response):
        pass
