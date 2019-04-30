# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


class HuludaoxinwenwangSpider(scrapy.Spider):
    name = 'huludaoxinwenwang'
    allowed_domains = ['hldnews']
    start_urls = ['http://www.hldnews.com/hldyw/']
    def parse(self, response):
        res = response.xpath('/html/body/div[3]/div[2]/div[3]/ul/li/a/@href').extract()
        res1 = response.xpath('//*[@id="pe100_page_通用信息列表_普通式"]/a[1]/@href').extract_first()
        for url in res:
            url = 'http://www.hldnews.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

        i = re.findall(r'hldyw/List_(.*).html',res1)[0]
        for j in range(int(i)-20,int(i)):
            url = 'http://www.hldnews.com/hldyw/List_{}.html'.format(j)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get_detail_url(self,response):
        res = response.xpath('/html/body/div[3]/div[2]/div[3]/ul/li/a/@href').extract()
        for url in res:
            url = 'http://www.hldnews.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

    def get_detail(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//h1/span/font/text()").extract()[0]
        item['time'] = response.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div[1]/text()[3]').extract_first()
        item['content'] = response.xpath('//*[@id="articleContnet"]/div/text()').extract()
        item['come_from'] = response.xpath("/html/body/div[3]/div[2]/div[3]/div[2]/div[1]/a[2]/text()").extract_first()
        if item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split('发布时间：')[1].split('点击数：')[0].replace('年','/').replace('月','/').replace('日','')
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '葫芦岛新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['env_num'] = '0'
            item['read_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '葫芦岛'
            item['addr_province'] = '辽宁省'
            print(item)
            # yield item
