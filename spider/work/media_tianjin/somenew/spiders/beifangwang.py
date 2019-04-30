# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


# =============================================================================
# 北国网爬虫
# =============================================================================


class TianjinSpider(scrapy.Spider):
    name = 'beifangwang'
    allowed_domains = ['enorth.com.cn']
    start_urls = ['http://news.enorth.com.cn/tj/tjyw/','http://news.enorth.com.cn/tj/wytd/',\
                  'http://news.enorth.com.cn/tj/fwkx/tianqixinxi/','http://news.enorth.com.cn/tj/jiaoyuxinxi/',\
                  'http://news.enorth.com.cn/tj/fwkx/bianmin/','http://news.enorth.com.cn/tj/tjrenshi/index.shtml',\
                  'http://news.enorth.com.cn/tj/txyg/index.shtml','http://news.enorth.com.cn/tj/chengjianxinwen/',\
                  'http://news.enorth.com.cn/tj/fazhixinwen/','http://news.enorth.com.cn/gn/gnyw/',\
                  'http://news.enorth.com.cn/gn/gdzl/','http://news.enorth.com.cn/gn/gat/',\
                  'http://news.enorth.com.cn/gn/ssqd/','http://news.enorth.com.cn/net/',\
                  'http://news.enorth.com.cn/gj/gjyw/','http://news.enorth.com.cn/gj/sspl/',\
                  'http://news.enorth.com.cn/gj/qqzh/','http://news.enorth.com.cn/gj/jsjj/',\
                  'http://news.enorth.com.cn/sh/alcz/','http://news.enorth.com.cn/sh/qwqs/',\
                  'http://news.enorth.com.cn/sh/shrw/','http://news.enorth.com.cn/tj/fwkx/jiaotongxinxi/',\
                  'http://news.enorth.com.cn/tj/jiaoyuxinxi/','http://news.enorth.com.cn/tj/fwkx/bianmin/',\
                  'http://news.enorth.com.cn/tj/qxdt/','http://news.enorth.com.cn/tj/dushixiaofei/',\
                  'http://news.enorth.com.cn/tj/tjyw/tjshiwei/index.shtml','http://news.enorth.com.cn/tj/tjyw/tjrenda/index.shtml',\
                  'http://news.enorth.com.cn/tj/tjyw/tjzhengfu/index.shtml','http://news.enorth.com.cn/tj/tjyw/tjzhengxie/index.shtml','http://www.enorth.com.cn/']


    def parse(self, response):
        print(len(response.url), response.url)
        res = response.xpath('/html/body/table[3]/tr[1]/td[3]/table/tr[5]/td/table/tr/td/a/@href').extract()
        for url in res:
            if '2015' not in url:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)
        if len(response.url) == 25:
            res = response.xpath('/html/body/div/div[11]/div[1]/div/table/tr/td/a/@href|/html/body/div/div[18]/div[1]/div[2]/div/span/table/tr/td/a/@href|//div/div/div/span/table/tr/td/a/@href|/html/body/div/div/div/div/div/div/div/table/tr/td/a/@href').extract()
            for url in res:
                if 'thread' not in url:
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url, '我是响应的rul')
        item['title'] = response.xpath('//*[@id="title"]/div/h2').xpath('string(.)').extract_first()
        try:
            item['time'] = response.xpath('//*[@id="title"]/div[2]/p/span[4]/text()').extract()[0]
        except:
            pass
        item['content'] = response.xpath('//*[@id="article"]/div[2]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('//*[@id="title"]/div[2]/p/span[1]/text()|//*[@id="title"]/div[2]/p/span[1]/a/text()').extract()
        if item['title'] and item['content']:
            item['title'] = ''.join(item['title'].split('扫码阅读手机版')[0].split())
            print(len(item['come_from']), item['come_from'], '11111111111111111111111111111111111111111111111111')
            if len(item['come_from']) == 1:
                item['come_from'] = item['come_from'][0].split('来源：')[1]
                if '\n' in item['come_from']:
                    item['come_from'] = item['come_from'].split('\n')[2]
            elif len(item['come_from']) == 3:
                item['come_from'] = item['come_from'][1]
            else:
                item['come_from'] = item['come_from'][2]

            item['time'] = item['time'].split('\xa0\xa0')[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                             '').replace(
                '\u2002', '').replace('\t', '').replace('\r', '').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '北国网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '天津'
            item['addr_province'] = '天津'
            print('北国网' * 100)
            print(item)



