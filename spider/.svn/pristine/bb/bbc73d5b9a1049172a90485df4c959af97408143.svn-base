# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 晋中新闻网爬虫 首页:
# =============================================================================


class JinzhongxinwenwangSpider(scrapy.Spider):
    name = 'jinzhongxinwenwang'
    allowed_domains = ['sxjzxww.com']
    start_urls = ['http://www.sxjzxww.com/quxian/','http://www.sxjzxww.com/shanxi/','http://www.sxjzxww.com/jinzhong/','http://www.sxjzxww.com/guonei/','http://www.sxjzxww.com/guoji/']


    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('/html/body/div/div[2]/div[1]/div/p/a/@href').extract()
        for url in res:
            url = 'http://www.sxjzxww.com'+url
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,6):
            url = response.url +'index-{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url)
        if 'quxian' in response.url :
            for i in range(6,200):
                url = 'http://www.sxjzxww.com/list-14-0-0-0-{}.aspx'.format(i)
                yield scrapy.Request(url, callback=self.get_detail_url)
        if 'jinzhong' in response.url:
            for i in range(6,200):
                url = 'http://www.sxjzxww.com/list-15-0-0-0-{}.aspx'.format(i)
                yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self,response):
        res = response.xpath('/html/body/div/div[2]/div[1]/div/p/a/@href').extract()
        for url in res:
            url = 'http://www.sxjzxww.com' + url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/p/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/font/text()').extract()[0]
        item['content'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[6]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/font/text()').extract()[0]
        if  item['title'] and item['content']:
            item['time'] = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",item['time'])[0]
            item['url'] = response.url
            item['come_from'] = item['come_from'].split()[0]
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '晋中新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '晋中'
            item['addr_province'] = '山西省'
            print('晋中新闻网' * 100)
        print(item)












