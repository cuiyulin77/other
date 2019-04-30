# -*- coding: utf-8 -*-
import scrapy


class SinanewSpider(scrapy.Spider):
    name = 'sinaNew'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

    def parse(self, response):
        pass
