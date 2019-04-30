# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 长治新闻网爬虫 首页:
# =============================================================================


class ChangzhixinwenwangSpider(scrapy.Spider):
    name = 'changzhixinwenwang'
    allowed_domains = ['changzhinews.com']
    start_urls = ['http://www.changzhinews.com/']


    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('//div[@class="main1-2"]/div/a/@href|/html/body/div[2]/div/div/table/tr/td/a/@href').extract()
        for url in res:
            url = 'http://www.changzhinews.com'+url
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('/html/body/p[1]/text()').extract_first()
        item['time'] = response.xpath('/html/body/table[1]/tr/td[1]/text()[1]').extract()[0]
        item['content'] = response.xpath('//*[@id="kzzt"]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('/html/body/table[1]/tr/td[1]/a/text()').extract()[0]
        if  item['title'] and item['content']:
            item['time'] = item['time'].split('\xa0\xa0')[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '长治新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '长治'
            item['addr_province'] = '山西省'
            print('长治新闻网' * 100)
            yield item
















        
