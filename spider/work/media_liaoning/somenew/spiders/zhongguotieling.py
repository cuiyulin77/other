# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


class ZhongguotielingSpider(scrapy.Spider):
    name = 'zhongguotieling'
    allowed_domains = ['tielingcn']
    start_urls = ['http://www.tielingcn.com/news/news01/news0101/','http://www.tielingcn.com/news/news01/news0102/','http://www.tielingcn.com/news/news02/news0201/',\
                  'http://www.tielingcn.com/news/news01/news0109/','http://www.tielingcn.com/news/news01/news0108/','http://www.tielingcn.com/news/news02/news0203/',\
                  'http://www.tielingcn.com/news/news01/']

    def parse(self, response):
        for i in range(1,10):
            for i in range(1,10):
                url = response.url +'{}.shtml'.format(i)
                print(url)
                yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
        if len(response.url) == 37:
            res = response.xpath('//*[@id="content"]/div[1]/div[1]/div/ul/li/div/a/@href').extract()
            # print(res)
            for url in res:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/div/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()
        try:
            item['title'] = response.xpath("//*[@id=\"content\"]/div[1]/div[1]/div[2]/div[1]/text()").extract()[0]
        except:
            pass
        item['time'] = response.xpath('//*[@id="pubtime_baidu"]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div[2]/div[3]/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id=\"source_baidu\"]/text()").extract_first()
        if item['content'] and item['time']:
            item['time'] = item['time'].replace('年','/').replace('月','/').replace('日','')
            item['come_from'] = item['come_from'].split('\r\n')[1].strip()
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '中国铁岭网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '铁岭'
            item['addr_province'] = '辽宁省'
            yield item