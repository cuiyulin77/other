# -*- coding: utf-8 -*-

import scrapy
import re
import json
import logging
import datetime
import time
from copy import deepcopy
import hashlib
from somenew.items import SomenewItem

# 此爬虫爬的太快，会爬不到数据
class QqnewsSpider(scrapy.Spider):
    name = 'qqnews'
    allowed_domains = ['qq.com']
    start_urls = ['http://ent.qq.com/articleList/rolls/']

    # 获取今日之前若干天的日期列表
    today = datetime.date.today()
    # print('*****', today)
    url_list = []
    for i in range(100):
        date = today - datetime.timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        # dates.append(date)
        # 获取新闻，娱乐，体育，财经，科技，汽车，教育，房产
        taglist = ['ent', 'sports', 'finance', 'tech','news','house','auto']
        for tag in taglist:
            for j in range(10):
                url = 'http://roll.news.qq.com/interface/cpcroll.php?site=' + tag + '&mode=1&cata=&date=' + date + '&page={}'.format(j)
                url_list.append(url)


    def parse(self, response):
        for url in self.url_list:
            yield scrapy.Request(url, callback=self.parsepage,  dont_filter=True)

    def parsepage(self, response):
        newsjson = json.loads(response.text)
        newslist = newsjson['data']['article_info']
        for news in newslist:
            url = news['url']
            meta = {
                'title': news['title'],
                'pubtime': news['time'],
            }
            yield scrapy.Request(url, callback=self.parsebody, dont_filter=True, meta=deepcopy(meta))

    def parsebody(self, response):
        meta = response.meta
        item = SomenewItem()
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['title'] = meta['title']
        item['url'] = response.url
        item['content'] = '\n'.join(
            response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@class='text']/text()").extract())
        item['time'] = meta['pubtime']
        item['media'] = '腾讯新闻'
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        if not item['content'] == '':
            yield item
