# -*- coding: utf-8 -*-
import scrapy
import json
from somenew.items import SomenewItem
from copy import deepcopy
import hashlib
import datetime

# 新京报爬虫
# 此爬虫是使用json获取url等信息，也可以在http://epaper.bjnews.com.cn/获取电子报的页面，从中获取报纸信息
class XinjingbaoSpider(scrapy.Spider):
    name = 'xinjingbao'
    allowed_domains = ['bjnews.com.cn']
    json_url_list = []
    for i in range(10)[1:]:
        url = 'http://www.bjnews.com.cn/webapi/hotlist?page=' + str(i) + '&t=0.32387063277519945'
        json_url_list.append(url)
    start_urls = json_url_list

    def parse(self, response):
        ret = response.body.decode()
        dict = json.loads(ret)
        data_list = dict['data']
        for data in data_list:
            item = SomenewItem()
            item['time'] = data['submit_time']
            item['title'] = data['title']
            item['url'] = data['url']
            yield scrapy.Request(item['url'], callback=self.get_content, meta={'item': deepcopy(item)})

    def get_content(self, response):
        item = response.meta['item']
        item['media'] = response.xpath("(//span[@class='author'])[1]/text()").extract_first()
        content = response.xpath("//div[@class='content']")
        item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item