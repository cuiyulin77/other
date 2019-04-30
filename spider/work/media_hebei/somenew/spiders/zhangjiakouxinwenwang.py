# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class ZhangjiakouxinwenwangSpider(scrapy.Spider):
    name = 'zhangjiakouxinwenwang'
    allowed_domains = ['zjknews.com']
    start_urls = ['http://www.zjknews.com/xianqu/','http://www.zjknews.com/news/','http://www.zjknews.com/news/shizheng/']
    custom_settings = {'DOWNLOAD_DELAY': 0.1}
    #
    def parse(self, response):
        print(len(response.url))
        # 新闻页面上面含有news标题的url
        if len(response.url) == 28:
            res = response.xpath('/html/body/div[1]/div/div[3]/div/ul/li/a/@href').extract()
            for url in res:
                if 'news' in url and 'http' not in url:
                    url = 'http://www.zjknews.com'+url
                    yield scrapy.Request(url, callback=self.get_detail_url)


        # 区县
        if len(response.url) == 30:
            res = response.xpath('//*[@id="xianqu"]/div/div/div/div/div/ul/li/a/@href').extract()
            for url in res:
                print(url)
                url = 'http://www.zjknews.com'+url
                yield scrapy.Request(url, callback=self.get_detail)


        # 时政
        if len(response.url) == 37:
            res = response.xpath('/html/body/div[5]/div[1]/ul/li/a/@href|/html/body/div[5]/div[2]/div[2]/div[1]/a/@href').extract()
            for url in res:
                url = 'http://www.zjknews.com' + url
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)
            for i in range(2,10):
                url ='http://www.zjknews.com/news/shizheng/index_%d.html'% i
                yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self, response):
        res = response.xpath('/html/body/div[5]/div[1]/ul/li/a/@href').extract()
        for url in res:
            url = 'http://www.zjknews.com' + url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[4]/h1/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[4]/div[2]/span/text()').extract_first()
        item['content'] = response.xpath('/html/body/div[5]/div[1]/div[1]/p[3]/text()|/html/body/div[5]/div[1]/div[1]/p/text()\
                                         |/html/body/div[5]/div[1]/div[1]/p/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[4]/div[2]/span/a/text()').extract_first()
        if item['title'] and item['content']:
            item['url'] = response.url
            item['time'] = item['time'].split('\xa0\xa0')[0]
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '张家口新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            item['addr_city'] = '张家口'
            print('张家口新闻网'* 100)
            print(item)
            yield item
