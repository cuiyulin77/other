# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json



class LiaoningtiebaSpider(scrapy.Spider):
    name = 'liaoningtieba'
    allowed_domains = ['jj']
    start_urls = ['http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81']

    def parse(self, response):
        # http://tieba.baidu.com
        # res = response.xpath('//li/div/div/div/div/a/@href').extract()
        # for url in res:
        #     url = 'http://tieba.baidu.com'+url
        #     if 'ie=utf-8' not in url:
        #         yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
        for i in range(1,500):
            url = 'http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81&ie=utf-8&pn={}'.format(50*i)
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get_detail_url(self,response):
        res = response.xpath('//li/div/div/div/div/a/@href').extract()
        for url in res:
            url = 'http://tieba.baidu.com'+url
            if 'ie=utf-8' not in url:
                yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="j_core_title_wrap"]/div[2]/h1/text()').extract_first()
        item['time'] = re.findall(r';date&quot;:&quot;(.*?)&quot;,&quot;vote_crypt&quot;:',response.body.decode())[0]
        item['content'] = response.xpath('//div[1]/div/div/cc/div[2]/text()').extract()
        item['come_from'] = '百度贴吧'
        if  item['title'] and item['content'] and item['time']:
            for i in item['content']:
                item['content'] = i.strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '百度贴吧'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = None
            item['addr_province'] = '全国'
            print('辽宁新闻网' * 100)
            yield item

