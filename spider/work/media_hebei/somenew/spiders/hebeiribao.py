# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class YanzhaodushibaoSpider(scrapy.Spider):
    name = 'hebeiribao'
    allowed_domains = ['hebnews.cn']
    start_urls = ['http://hbrb.hebnews.cn/pc/paper/layout/201811/20/node_01.html']

    def parse(self, response):
            for j in range(1,13):
                for x in range(1,31):
                    url = 'http://yzdsb.hebnews.cn/pc/paper/layout/2018%02d/%02d/node_01.html'%(j,x)
                    yield scrapy.Request(url, callback=self.get_detail_url)


    def get_detail_url(self,response):
        res = response.xpath('//*[@id="layoutlist"]/li/a/@href').extract()
        for url in res:
            url = response.url.split('node_01.htm')[0]+url
            yield scrapy.Request(url, callback=self.get_detail_url_list)

    def get_detail_url_list(self,response):
        res = response.xpath('//*[@id="articlelist"]/li/a/@href').extract()
        for url in res:
            key = url[-12:]
            if '/' in key:
                url = response.url[0:49].replace('layout','c') + key
                yield scrapy.Request(url, callback=self.get_detail)
            else:
                url = response.url[0:50].replace('layout','c')+key
                yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('//*[@id="Title"]/text()').extract_first()
        item['time'] = response.url.split('/paper/c/')[1][:9].replace('8','8/')
        item['content'] = response.xpath('//*[@id="ozoom"]/founder-content/p/text()').extract()
        item['come_from'] = '河北日报'
        if item['title'] and item['content']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '河北日报'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            # print('燕赵都市报' * 100)

            yield item
