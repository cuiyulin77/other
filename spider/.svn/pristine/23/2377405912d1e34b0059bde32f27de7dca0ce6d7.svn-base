# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime



class BaodingzaixianSpider(scrapy.Spider):
    name = 'baodingzaixian'
    allowed_domains = ['bdzx.com.cn']
    start_urls = ['http://news.bdzx.com.cn/shehui/','http://news.bdzx.com.cn/hebei/','http://news.bdzx.com.cn/baoding/','http://news.bdzx.com.cn/baoliao/']


    def parse(self, response):
        res = response.xpath('//*[@id="category"]/div/div/em/a/@href').extract()
        for url  in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)


        for url in range(2,5):
            url = response.url+ '{}.html'.format(url)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="category"]/div/div/em/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[5]/div[1]/div[1]/div/h1/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/span[1]/text()').extract()[0]
        item['content'] = response.xpath('/html/body/div[5]/div[1]/div[1]/div/div[2]/p/text()[1]').extract()
        item['come_from'] = '保定在线'

        if item['title'] and item['content']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '保定在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            item['addr_city'] = '保定'
            print('保定在线'*100)
            print(item)
            yield item








