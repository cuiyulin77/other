# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class HuanbohaixinwenwangSpider(scrapy.Spider):
    name = 'huanbohaixinwenwang'
    allowed_domains = ['huanbohainews.com.cn']
    start_urls = ['http://tangshan.huanbohainews.com.cn/xqbd/index.shtml','http://tangshan.huanbohainews.com.cn/zhxw/index.shtml'\
        ,'http://tangshan.huanbohainews.com.cn/szyw/index.shtml','http://tangshan.huanbohainews.com.cn/shxw/index.shtml'\
        ,'http://tangshan.huanbohainews.com.cn/wmsj/index.shtml','http://tangshan.huanbohainews.com.cn/wmsj/index.shtml'\
                  ,'http://news.huanbohainews.com.cn/hbh/index.shtml','http://news.huanbohainews.com.cn/gn/index.shtml'\
                  ,'http://news.huanbohainews.com.cn/sh/index.shtml',]

    def parse(self, response):
        res = response.xpath('/html/body/table[4]/tr/td[1]/table/tr/td/a/@href').extract()
        if res:
            for url in res:
                yield scrapy.Request(url, callback=self.get_detail_url)
        yield scrapy.Request(response.url, callback=self.get_detail_url)
    def get_detail_url(self, response):
        res = response.xpath('/html/body/table[4]/tr/td[1]/table/tr[1]/td[2]/table/tr/td/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
            print(response.url, '我是响应的rul')
            item = SomenewItem()
            item['title'] = response.xpath('/html/body/table[3]/tr[2]/td[1]/table[2]/tr/td/table[1]/tr/td/div/h1/text()').extract()[0]
            item['time'] = response.xpath('//td[@class="STYLE2 zi12"]/text()').extract()[1]
            item['come_from'] = response.xpath('//td[5]/a/span/text()').extract_first()
            item['content'] = response.xpath('//td/p/text()').extract()
            if item['title'] and item['content']:
                item['come_from'] = item['come_from'].split('来源：')[1]
                item['time'] = item['time'].split('\r\n')[1]
                item['url'] = response.url
                item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                                 '').replace(
                    '\u2002', '').replace('\t', '').replace('\r', '').strip()
                m = hashlib.md5()
                m.update(str(item['url']).encode('utf8'))
                item['article_id'] = m.hexdigest()
                item['media'] = '环渤海新闻网'
                item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                item['comm_num'] = "0"
                item['fav_num'] = '0'
                item['read_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '网媒'
                item['addr_province'] = '河北省'
                item['addr_city'] = '唐山'
                print('环渤海新闻网' * 100)
                yield item

