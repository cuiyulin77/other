# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 朔州新闻网爬虫 首页:
# =============================================================================


class SuozhouxinwenwangSpider(scrapy.Spider):
    name = 'suozhouxinwenwang'
    allowed_domains = ['sxsznews.com']
    start_urls = ['http://www.sxsznews.com/']
    custom_settings = {'DOWNLOAD_DELAY': 0.1}

    def parse(self, response):
        res = response.xpath('//*[@id="menu_nav"]/li/a/@href').extract()
        a= ['73','658','107','75','651','index_szrb.shtml','69','88','106','144']
        b = []
        for url in res:
            for i in a:
                if i in url:
                    b.append(url)
        ret_list = list(set(res) ^ set(b))
        for url in ret_list:
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('/html/body/div[4]/div[2]/div[1]/div/div[1]/ul/li/a/@href').extract()
        print(res)
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,5):
            url = 'http://www.sxsznews.com/html/54/list-{}.shtml'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url1)
    def get_detail_url1(self,response):
        res = response.xpath('/html/body/div[4]/div[2]/div[1]/div/div[1]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/text()').extract_first()
        item['come_from'] = response.xpath('//span[1]/text()').extract()[1]
        item['content'] = response.xpath('//*[@id="content"]/p/text()').extract()
        item['time'] = response.xpath('//div[@class="ac_fl"]/span/text()').extract()
        if  item['title'] and item['content'] and item['time']:
            item['come_from']= item['come_from'].split('来源：')[1]
            for url in item['time']:
                b  = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", url)
                if b:
                    item['time'] = b[0]
            item['url'] = response.url
            item['time']= item['time']
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '朔州新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '朔州'
            item['addr_province'] = '山西省'
            print('朔州新闻网' * 100)
            yield item

