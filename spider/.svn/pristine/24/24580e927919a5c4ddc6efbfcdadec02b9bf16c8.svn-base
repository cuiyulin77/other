# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class ChangzhouxinwenwangSpider(scrapy.Spider):
    name = 'hengshuixinwenwang'
    allowed_domains = ['hsrb.com.cn']
    start_urls = ['http://www.hsrb.com.cn/a/news/hengshuishizheng/','http://www.hsrb.com.cn/a/news/hengshuishizheng/',\
                  'http://www.hsrb.com.cn/a/news/hengshuixinwen/','http://www.hsrb.com.cn/a/xianshiqu/',\
                  'http://www.hsrb.com.cn/a/news/pinglun/']
    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('/html/body/div[1]/table[2]/tr/td[2]/table/tr[2]/td/table/tr[1]/td[2]/table/tr/td[1]/a/@href').extract()
        for url in res:
            url = 'http://www.hsrb.com.cn'+url
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail_url(self,response):
        """新闻分类url提取"""
        res = response.xpath('//div[1]/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[1]/table/tr/td[1]/table/tr/td/table[2]/tr[1]/td/div/h2/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[1]/table/tr/td[1]/table/tr/td/table[2]/tr[2]/td/div/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[1]/table/tr/td[1]/table/tr/td/table[2]/tr[2]/td/div/text()').extract()
        item['content'] = response.xpath('/html/body/div[1]/table/tr/td/table/tr/td/table/tr/td/p/span/text()\
        |/html/body/div[1]/table/tr/td[1]/table/tr/td/table[2]/tr[3]/td/text()|/html/body/div[1]/table/tr/td[1]/table/tr/td/table[2]/tr[3]/td/div/text()').extract()
        if item['title'] and item['content']:
            item['come_from'] = item['come_from'][2]
            for node in item['time']:
                data = re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', node)
                if data:
                    item['time'] = data[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '衡水新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            item['addr_city'] = '衡水'
            print('衡水新闻网'*100)
            yield item
            print(item)


