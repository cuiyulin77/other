# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class HandanxinwenwangSpider(scrapy.Spider):
    name = 'handanxinwenwang'
    allowed_domains = ['handannews.com.cn']
    start_urls = ['http://www.handannews.com.cn/news/column/node_75.html',\
                  'http://www.handannews.com.cn/zhengwu/column/node_2.html',\
                  'http://www.handannews.com.cn/news/column/node_60.html',\
                  'http://www.handannews.com.cn/news/column/node_61.html',\
                  'http://www.handannews.com.cn/news/column/node_62.html',\
                  'http://www.handannews.com.cn/news/column/node_64.html',\
                  'http://www.handannews.com.cn/news/column/node_65.html',\
                  'http://www.handannews.com.cn/news/column/node_63.html',\
                  'http://www.handannews.com.cn/news/column/node_66.html',\
                  'http://www.handannews.com.cn/news/column/node_69.html',\
                  'http://www.handannews.com.cn/news/column/node_68.html',\
                  'http://www.handannews.com.cn/news/column/node_71.html',\
                  'http://www.handannews.com.cn/news/column/node_70.html']


    def parse(self, response):
        res = response.xpath('//ul/li/div/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,11):
            # url = response.url + '_{}.html'.format(i)
            a = '_'+str(i)+'.'+'html'
            url = response.url.replace('.html',a)
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self, response):
        res = response.xpath('//ul/li/div/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[3]/h1/text()').extract_first()
        item['time'] = response.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="artibody"]/p/text()').extract()
        try:
            item['come_from'] = response.xpath('//*[@id="top_bar"]/div/div[2]/a/text()').extract()[0]
        except:
            pass
        if item['title'] and item['content']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '邯郸新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            print('邯郸新闻网' * 100)
            yield item
