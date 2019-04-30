# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json



class FuxinzaixianSpider(scrapy.Spider):
    name = 'fuxinzaixian'
    allowed_domains = ['fuxin.ccoo.cn']
    start_urls = ['http://www.fuxin.ccoo.cn/tieba/']

    def parse(self, response):
        for i in range(1,6):
            url = 'http://www.fuxin.ccoo.cn/tieba/index-0-{}-1.html'.format(i)
        yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)


    def get_detail_url(self,response):
        res = response.xpath('//*[@id="topiclist"]/div/div[1]/div[2]/div[1]/a/@href').extract()
        for url in res:
            url = 'http://www.fuxin.ccoo.cn'+url
            yield scrapy.Request(url, callback=self.get_detail_url_list, dont_filter=True)

    def get_detail_url_list(self,response):
        item = SomenewItem()
        item['time'] = response.xpath('//*[@id="topic_o"]/table/tr[1]/td[2]/div[1]/ul/li[3]/text()').extract_first().split('发表于：')[1]
        item['title'] = response.xpath('//*[@id="topic_title_100"]/div/div[1]/h1/text()').extract()
        item['content'] = response.xpath('//*[@id="topic_o"]/table/tr[1]/td[2]/div[3]/table/tr/td[1]/div/h3/text()|//*[@id="topic_o"]/table/tr[1]/td[2]/div[3]/table/tr/td[1]/div/text()\
        |//*[@id="topic_o"]/table/tr[1]/td[2]/div[3]/table/tr/td[1]/div/div[2]/p/text()|//div/table/tr/td/div/p/text()|//section/section/section/p/text()').extract()
        item['come_from'] = '阜新在线'
        if item['title'] and item['content'] and item['time']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',\
                                '').replace('\u2002', '').replace('\r', '').replace('\t','').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '阜新在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            yield item









