# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class HuanjingjinwangSpider(scrapy.Spider):
    name = 'huanjingjinwang'
    allowed_domains = ['010lf.com']
    start_urls = ['http://www.010lf.com/system/bjnews/','http://www.010lf.com/system/tjnews/'\
        ,'http://www.010lf.com/system/hbnews/','http://www.010lf.com/system/hbnews/lfnews/'\
        ,'http://www.010lf.com/system/txdg/','http://www.010lf.com/system/review/']
    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('/html/body/div/div[2]/div/div/div[1]/ul/li/div/h3/a/@href').extract()
        res2 = response.xpath('/html/body/div/div[2]/div/div/div[1]/div/div/span[position()>2]/a/@href').extract()
        for url in res:
            url = 'http://www.010lf.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
        for url in res2:
            print(len(url), url)
            if len(url) == 47:
                url = 'http://www.010lf.com'+url
                print(len(url),url)
                yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)


    def get_detail_url(self,response):
        res = response.xpath('/html/body/div/div[2]/div/div/div[1]/ul/li/div/h3/a/@href').extract()
        for url in res:
            url = 'http://www.010lf.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/text()').extract()
        item['content'] = response.xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/p/text()').extract()
        if item['title'] and item['content']:
            item['come_from'] = item['come_from'][0].split('|')[1].split('来源：')[1]
            item['time'] = item['time'][0].split('|')[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '环京津网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            print('环京津网'*100)
            yield item
            print(item)






