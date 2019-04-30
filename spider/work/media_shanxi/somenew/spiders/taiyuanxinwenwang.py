# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 太原新闻网爬虫 首页:
# =============================================================================


class TtaiyuanxinwenwangSpider(scrapy.Spider):
    name = 'taiyuanxinwenwang'
    allowed_domains = ['tynews.com.cn']
    start_urls = ['http://www.tynews.com.cn/']

    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('//*[@id="pcHeader"]/div/div[1]/a[position()>1 and position()<last()-2]/@href').extract()
        res1 = response.xpath('//*[@id="newsFocus"]/div/ul/li/a/@href|//div/span/ul/li/a/@href|//div/ul/span/li/a/@href').extract()
        for url in res1:
            if 'cms_udf' not in url:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="newslist"]/span/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="main"]/header/h1/text()|//*[@id="title"]/h1/text()').extract_first()
        item['time'] = response.xpath('//*[@id="title"]/div/span/text()|//*[@id="main"]/header/time/text()').extract()
        item['content']= response.xpath('//*[@id="main"]/div[position()>1]|//*[@id="article"]/div').xpath('string(.)').extract()
        item['come_from'] = response.xpath('//*[@id="main"]/header/span/a/text()|//*[@id="title"]/div/span[3]/text()|//*[@id="title"]/div/span[1]/a/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            for i in item['time']:
                if '年' in i:
                    item['time'] = i.replace('月','/').replace('日','').replace('年','/')
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '太原新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '太原'
            item['addr_province'] = '山西省'
            print('太原新闻网' * 100)
            yield item

