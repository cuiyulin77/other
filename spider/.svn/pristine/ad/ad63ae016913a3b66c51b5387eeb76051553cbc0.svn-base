# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
import datetime
from urllib import parse
import time
from copy import deepcopy
import hashlib
from somenew.items import SomenewItem

# 手机中国新闻爬虫
class CnmoSpider(scrapy.Spider):
    name = 'cnmo'
    allowed_domains = ['cnmo.com/']
    start_urls = ['http://cnmo.com/news/']
    # 获取今日之前若干天的日期列表
    today = datetime.date.today()
    # print('*****', today)
    url_list = []
    for i in range(2):
        date = today - datetime.timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        url = 'http://www.cnmo.com/news/date/'+ str(date)
        url_list.append(url)


    def parse(self, response):
        for url in self.url_list:
            yield scrapy.Request(url,callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,respose):
        # print('&'*100, 222222)
        url_list = respose.xpath("//div[@class='Newcon-title clearfix']/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url,callback=self.get_content,dont_filter=True)

    def get_content(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['time'] = response.xpath("//div[@class='ctitle_spe']/div[1]/span[3]/text()").extract_first()
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='ctext']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['media'] = response.xpath("//div[@class='ctitle_spe']/div[1]/b/text()").extract_first()
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        # m.update(str(item['url'])).encode('utf-8')
        item['article_id'] = article_id
        yield item


