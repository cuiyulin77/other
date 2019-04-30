# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 天涯论坛辽宁,鞍山，大连等爬虫 首页:
# =============================================================================



class TianyaluntanliaoningSpider(scrapy.Spider):
    name = 'tianyaluntanliaoning'
    allowed_domains = ['tianya']
    start_urls = ['http://bbs.tianya.cn/list-5045-1.shtml']

    def parse(self, response):
        res = response.xpath('//*[@id="bbs_left_nav"]/div[3]/ul/li/a/@href').extract()
        for url in res:
            url = 'http://bbs.tianya.cn'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="main"]/div[7]/table/tbody/tr/td[1]/a/@href').extract()
        for url in res:
            url = 'http://bbs.tianya.cn'+ url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)



    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract_first()
        item['time'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[2]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="bd"]/div[5]/div[1]/div/div[2]/div[position()<last()-2]/text()|//*[@id="bd"]/div[4]/div[1]/div/div[2]/div/text()').extract()
        item['come_from'] = '天涯论坛'
        if  item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split('时间：')[1]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '天涯论坛'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[3]/text()').extract_first()
            item['comm_num'] = item['comm_num'].split('点击：')[1]
            item['read_num'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[4]/text()').extract_first()
            # print(item['read_num'], '我是点击量')
            item['read_num'] = item['read_num'].split('回复：')[1]
            item['fav_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = None
            item['addr_province'] = '全国'
            # print('辽宁新闻网' * 100)
            # yield item


