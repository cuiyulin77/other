# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem
from copy import deepcopy

# 北京青年报爬虫
class BjqingnianSpider(scrapy.Spider):
    name = 'bjqingnian'
    allowed_domains = ['ynet.com']
    start_urls = ['http://news.ynet.com/list/1700t76.html','http://news.ynet.com/list/990t76.html']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='cfix fin_newsList']/li")
        print('1'*100)
        for li in li_list:
            item = SomenewItem()
            item['title'] = li.xpath("./h2/a/text()").extract_first()
            item['time'] = li.xpath(".//em[@class='fRight']/text()").extract_first()
            href = li.xpath("./h2/a/@href").extract_first()
            print('2' * 100)
            yield scrapy.Request(href,callback=self.get_content,meta={'item':deepcopy(item)})
        next_href = response.xpath("//li[@class='active']/a[text()='下一页']/@href").extract_first()
        if next_href is not None:
            print('3' * 100)
            yield scrapy.Request(next_href,callback=self.parse)

    def get_content(self,response):
        print('4' * 100)
        item = response.meta['item']
        item['url'] = response.url
        item['content'] = response.xpath("//div[@id='articleAll']/div/p").extract()
        item['media'] = '北京青年报'
        item['create_time'] = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item





