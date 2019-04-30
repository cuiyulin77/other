# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 运城新闻爬虫 首页:
# =============================================================================


class YunchengxinwenSpider(scrapy.Spider):
    name = 'yunchengxinwen'
    allowed_domains = ['sxycrb.com']
    start_urls = ['http://www.sxycrb.com/?category-143','http://www.sxycrb.com/?category-9'\
        ,'http://www.sxycrb.com/?category-7.html','http://www.sxycrb.com/?category-424.html'\
        ,'http://www.sxycrb.com/?category-40.html','http://www.sxycrb.com/?category-341.html'\
        ,'http://www.sxycrb.com/?category-286','http://www.sxycrb.com/?category-142'\
        ,'http://www.sxycrb.com/?category-6.html','http://www.sxycrb.com/?category-423.html',\
        'http://www.sxycrb.com/?category-422.html','http://www.sxycrb.com/?category-3']

    def parse(self, response):
        res = response.xpath('/html/body/div/div/div[3]/div[1]/div[1]/ul/li/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        if '143' in response.url:
            for i  in range(2,20):
                url = response.url+'-'+response.url.split('?')[1]+'-page-%s'%i
                yield scrapy.Request(url, callback=self.get_detail_url)


    def get_detail_url(self,response):
        res = response.xpath('/html/body/div/div/div[3]/div[1]/div[1]/ul/li/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="article"]/h1/text()').extract_first()
        item['time'] = response.xpath('//*[@id="article_extinfo"]/div[2]/text()').extract()[0]
        item['content'] = response.xpath('//*[@id="article_body"]').xpath('string(.)').extract()
        item['come_from'] = response.xpath('//*[@id="article_extinfo"]/div[1]/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split('\r\n时间：')[1].replace('年','/').replace('月','/').replace('日','')
            item['come_from']= item['come_from'].split('\n')[2]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '运城新闻'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '大同'
            item['addr_province'] = '山西省'
            print('运城新闻' * 100)
            yield item

