# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class DalianxinwenwangSpider(scrapy.Spider):
    name = 'dalianxinwenwang'
    allowed_domains = ['dlxww.com']
    start_urls = ['http://www.dlxww.com/']
    #
    def parse(self, response):
        res = response.xpath('/html/body/div[5]/div[2]/div[1]/div[4]/ul/li/a/@href|//div/h1/a/@href\
        |/html/body/div/div/div/div/ul/li/span/a/@href|/html/body/div/div/div/div/ul/li/a/@href\
        |/html/body/div[5]/div[2]/div/div/div/h2/a/@href\
        |/html/body/div[5]/div[2]/div/ul/li/span/a/@href').extract()
        res1 = response.xpath('/html/body/div[2]/div[2]/div/ul/li/a/@href').extract()
        for url in res:
            url = 'http://www.dlxww.com/'+url
            yield scrapy.Request(url, callback=self.get_detail)
        for url in res1:
            key = url.split('news/')[1].split('node_')[1].split('.htm')[0]
            print(key)
            url = 'http://www.dlxww.com/'+url
            yield scrapy.Request(url, callback=self.get_detail_url,meta={'key':key})

    def get_detail_url(self,response):
        res = response.xpath('/html/body/div[5]/div[1]/div/h2/a/@href|/html/body/div[4]/div[1]/a/@href').extract()
        for url in res:
            url ='http://www.dlxww.com/news/'+url
            yield scrapy.Request(url, callback=self.get_detail)
        print(response.url)
        for i  in  range(2,20):
            url ='http://www.dlxww.com/news/node_' + response.meta['key']+'_{}.htm'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url_list)


    def get_detail_url_list(self,response):
        res = response.xpath('/html/body/div[5]/div[1]/div/h2/a/@href|/html/body/div[4]/div[1]/a/@href').extract()
        for url in res:
            url ='http://www.dlxww.com/news/'+url
            yield scrapy.Request(url, callback=self.get_detail)




    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()
        item['title'] = response.xpath('/html/body/div[4]/div[1]/h1/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[4]/div[1]/div[1]/text()').extract_first()
        item['content'] = response.xpath('/html/body/div[4]/div[1]/div[2]/div/p/text()').extract()
        item['come_from'] = response.xpath("/html/body/div[4]/div[1]/div[1]/text()").extract_first()
        if item['title'] and item['content'] and item['time']:

            item['time'] = item['time'].split('\r\n')[0]
            # try:
            item['come_from'] = item['come_from'].split('\r\n')[1].strip()

            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',\
                                '').replace('\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '大连新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            item['addr_city'] = '大连'
            print('大连新闻网' * 100)
            yield item