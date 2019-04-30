# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 大同新闻网爬虫 首页:
# =============================================================================


class DatongxinwenwangSpider(scrapy.Spider):
    name = 'datongxinwenwang'
    allowed_domains = ['dtnews.cn']
    start_urls = ['http://www.dtnews.cn/bendi/','http://www.dtnews.cn/wangshiredian/','http://www.dtnews.cn/wenhua/','http://www.dtnews.cn/qiche/','http://www.dtnews.cn/jiaoyu/','http://www.dtnews.cn/licai/','http://www.dtnews.cn/wangshiredian/']

    def parse(self, response):
        res = response.xpath('//li/a/@href').extract()
        print(res)
        for url in res:
            url1 = 'http://www.dtnews.cn'+url
            yield scrapy.Request(url1, callback=self.get_detail)
        for i in range(2,5):
            url2 = response.url+'index_{}.html'.format(i)
            yield scrapy.Request(url2, callback=self.get_detail_url)
            print(url2)
    def get_detail_url(self,response):
        res = response.xpath('//li/a/@href').extract()
        print(res)
        for url in res:
            url1 = 'http://www.dtnews.cn'+url
            yield scrapy.Request(url1, callback=self.get_detail)

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//dl/dt/text()').extract_first().strip()
        item['time'] = response.xpath('//*[@id="zuozhe"]/span/text()').extract()[0]
        item['content'] = response.xpath('//div[@class="news_cont"]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('//*[@id="zuozhe"]/div/span/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            item['come_from']= item['come_from'].split('来自： ')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '大同新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '大同'
            item['addr_province'] = '山西省'
            print('大同新闻网' * 100)
            yield item
