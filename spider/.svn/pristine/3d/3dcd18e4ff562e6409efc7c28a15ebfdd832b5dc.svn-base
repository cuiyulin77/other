# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


class DandongxinwangSpider(scrapy.Spider):
    name = 'dandongxinwang'
    allowed_domains = ['jj']
    start_urls = ['http://www.ddhaihao.com/dandonglvyou/list_2_1.html']

    def parse(self, response):
        res = response.xpath('/html/body/div[1]/a/@href').extract()
        for url in res:
            if len(url)>30:
                yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get_detail_url(self,response):
        for i in range(1,7):
            for j in range(1,12):
                url = response.url.split('list')[0]+'list_{}_{}.html'.format(j,i)
                print(url)
                yield scrapy.Request(url, callback=self.get_detail_url_list, dont_filter=True)

    def get_detail_url_list(self, response):
        res = response.xpath('//ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

    def get_detail(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("string(//div[@class=\"mainarticle\"]/h1)").extract()[0]
        item['time'] = response.xpath('//span[1]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="main"]/div[1]/div[2]/div[2]/text()|//*[@id="main"]/div[1]/div[2]/div[2]/p/text()').extract()
        # item['come_from'] = response.xpath("//*[@id=\"main\"]/div[1]/div[2]/div[1]/div[1]/span[2]/text()").extract_first()
        if item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].replace('年','/').replace('月','/').replace('日','')
            item['come_from'] = '丹东新闻网'
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '丹东新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '丹东'
            item['addr_province'] = '辽宁省'
            print(item)
            yield item