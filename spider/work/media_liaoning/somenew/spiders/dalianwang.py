# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


class DaliantianjianwangSpider(scrapy.Spider):
    name = 'dalianwang'
    allowed_domains = ['dlv']
    start_urls = ['http://www.dlv.cn/']

    def parse(self, response):
        res = response.xpath('//div/div[2]/div/h1/a/@href|//div/h2/a/@href|//div/h3/a/@href\
        |//*[@id="channel"]/div/ul/li/a/@href|//div/div/div/div/a/@href|//div/div/div/div/a/@href').extract()
        res1 = response.xpath('/html/body/div[2]/div/ul[1]/li[1]/a/@href|//ul[2]/li[1]/a/@href').extract()
        if  res:
            for url in res:
                url = 'http://www.dlv.cn'+url
                if 'void' not in url:
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)


        if  res1:
            for url in res1:
                url = 'http://www.dlv.cn/' + url
                if len(url)>27:
                    # print(url)
                    yield scrapy.Request(url, callback=self.get_detail_url,dont_filter=True)

    def get_detail_url(self,response):
        res = response.xpath('//div/div/h2/a/@href').extract()
        for url in res:
            url = 'http://www.dlv.cn/'+url
            print(url,'我是url')
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

        for i in range(2,30):
            url = 'http://www.dlv.cn/news/dalian/index_{}.html'.format(i)
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url_list,dont_filter=True)
    def get_detail_url_list(self,response):
        res = response.xpath('//div/div/h2/a/@href').extract()
        for url in res:
            url = 'http://www.dlv.cn/'+ url
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

    def get_detail(self,response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//div/h2/text()').extract_first()
        item['time'] = response.xpath('//div/span[1]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="ctrlfscont"]/p/text()').extract()
        item['come_from'] = '大连网'
        if  item['title'] and item['content'] and item['time']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '大连网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['addr_province'] = '辽宁省'
            item['addr_city'] = '大连市'
            item['media_type'] = '网媒'
            # yield item
            print(item)
            print('大连网' * 100)


