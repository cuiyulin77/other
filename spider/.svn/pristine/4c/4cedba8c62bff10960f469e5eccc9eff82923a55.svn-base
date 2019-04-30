# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 忻州网爬虫 首页:
# =============================================================================

class XizhouwangSpider(scrapy.Spider):
    name = 'xizhouwang'
    allowed_domains = ['xinzhou.org']
    start_urls = ['http://news.xinzhou.org/html/gngj/','http://news.xinzhou.org/html/xznews/'\
        ,'http://news.xinzhou.org/html/sxdt/','http://news.xinzhou.org/html/xznews/xzws/'\
        ,'http://news.xinzhou.org/html/xznews/mshd/','http://news.xinzhou.org/html/xznews/xzbmdt/'\
        ,'http://news.xinzhou.org/html/xznews/xzbmdt/','http://news.xinzhou.org/html/xznews/xzhysc/'\
        ,'http://news.xinzhou.org/html/xznews/xzwh/','http://news.xinzhou.org/html/xznews/xzrw/'\
        ,'http://news.xinzhou.org/html/sndx/','http://xinzhou.org/index.php?m=content&c=index&a=lists&catid=568']
    custom_settings = {'DOWNLOAD_DELAY': 0.1}

    def parse(self, response):
        print(response.url,len(response.url))
        res = response.xpath('/html/body/div[4]/div[5]/div/h5/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url)
        if len(response.url)==64:
            res1 = response.xpath('/html/body/div[6]/div[1]/div[2]/div[1]/div[1]/div/ul/li/a[2]/@href').extract()
            for url in res1:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)


    def get_detail_url(self,response):
        print(response.url)
        res = response.xpath('//div[@class="col-left"]/ul/li/div[1]/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            try:
                yield scrapy.Request(url, callback=self.get_detail)
            except:
                pass

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="Article"]/h1[1]/text()').extract_first()
        item['come_from'] = response.xpath('//*[@id="Article"]/h1[2]/span[1]/a[1]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="Article"]/div').xpath('string(.)').extract()
        item['time'] = response.xpath('//*[@id="Article"]/h1[2]/span[1]/text()[1]').extract()
        if  item['title'] and item['content'] and item['time']:
            item['time'] = item['time'][0].split('\u3000')[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '忻州网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '忻州'
            item['addr_province'] = '山西省'
            print('忻州网' * 100)
            yield item





