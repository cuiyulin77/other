# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime



class QinhuangdaoxinwenwangSpider(scrapy.Spider):
    name = 'qinhuangdaoxinwenwang'
    allowed_domains = ['qhdnews']
    start_urls = ['http://www.qhdnews.com/cat/2','http://www.qhdnews.com/cat/4/p/3','http://www.qhdnews.com/cat/4/p/1'\
        ,'http://www.qhdnews.com/cat/4/p/2']


    def parse(self, response):
        res = response.xpath('/html/body/div[7]/div/div[3]/div/ul/li/a/@href').extract()
        for url  in res:
            url = 'http://www.qhdnews.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

    def get_detail_url(self,response):
        res = response.xpath('/html/body/div[6]/div/div[2]/div/ul/li/a/@href').extract()
        for url  in res:
            yield scrapy.Request(url, callback=self.get_detai,dont_filter=True)


    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[6]/div/div[2]/div[1]/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[6]/div/div[2]/div[2]/text()').extract()[0]
        item['content'] = response.xpath('//*[@id="body"]/p/text()').extract()
        item['come_from'] = '秦皇岛新闻网'

        if item['title'] and item['content']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '秦皇岛新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            item['addr_city'] = '秦皇岛'
            print('秦皇岛新闻网'*100)
            print(item)
            yield item



