# -*- coding: utf-8 -*-
import scrapy
from governmental_agencies.items import GovernmentalAgenciesItem
import time



class BeijingshizhengfuSpider(scrapy.Spider):
    name = 'beijingshizhengfu'
    allowed_domains = ['beijing.gov.cn']
    start_urls = ['http://www.beijing.gov.cn/']

    def parse(self, response):
        res= response.xpath('/html/body/div[3]/div[8]/div[1]/ul/li/a/text()').extract()
        item = GovernmentalAgenciesItem()
        for url in res:
            item['organizations_name'] = url.replace('市','北京市')
            item['province'] = '北京市'
            item['city'] ='北京市'
            item['county'] = None
            item['town'] = None
            item['url'] = response.url
            time_now = int(time.time())
            time_local = time.localtime(time_now)
            time_local = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            item['update_time'] = time_local
            yield item
        return item







