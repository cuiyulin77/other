# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json
from w3lib.html import remove_tags
import datetime


# =============================================================================
# 天津日报爬虫
# =============================================================================


class TianjinribaoSpider(scrapy.Spider):
    name = 'tianjinribao'
    allowed_domains = ['tianjinwe.com']
    start_urls = ['http://epaper.tianjinwe.com/tjrb/html/2018-12/18/node_1.htm?v=1']


    def parse(self, response):
            nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            daystop = nowtime.split()[0].split('-')[-1]
            monthstop = nowtime.split()[0].split('-')[-2]
            print(monthstop,daystop)
            for j in range(int(monthstop),int(monthstop)+1):
                for x in range(int(daystop),int(daystop)+1):
                    url = 'http://epaper.tianjinwe.com/tjrb/html/2019-%02d/%02d/node_1.htm?v=1'%(j,x)
                    yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="pageLink"]/@href').extract()
        for url in res:
            url = response.url.split('node_1.htm')[0]+url
            yield scrapy.Request(url, callback=self.get_detail_url_list)

    def get_detail_url_list(self,response):
        res = response.xpath('//div/a/@href').extract()
        for url in res:
            url = response.url.split('node')[0]+url
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('//td[@class="font01"]/text()').extract()[1]
        item['time'] = response.url.split('html/')[1][:10].replace('-','/')
        content = response.xpath("//*[@id=\"ozoom\"]/founder-content").extract()
        content = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u200b', u' ')
        content = remove_tags(content)
        item['content'] = content
        item['come_from'] = '天津日报'
        if item['title'] and item['content']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '天津日报'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '天津'
            item['addr_city'] = '天津'
            yield item







