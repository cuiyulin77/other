# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
import datetime
from copy import deepcopy
import hashlib
from somenew.items import SomenewItem

# 手机中国新闻爬虫
class CnmoSpider(scrapy.Spider):
    name = 'cnmo'
    allowed_domains = ['cnmo.com']
    url_list = ['http://www.cnmo.com/news/']

    for i in range(10)[2:]:
        url = 'http://www.cnmo.com/news/{}/'.format(i)
        url_list.append(url)
    start_urls = url_list


    def parse(self, response):
        h4_list = response.xpath("//div[@class='cobox']/div/div[2]/h4")
        print(response.url)
        for head in h4_list:
            item = SomenewItem()
            url = head.xpath("./a/@href").extract_first()
            item['title'] = head.xpath("./a/@title").extract_first()
            yield scrapy.Request(url,callback=self.parse_detail,meta={"item":item})



    def parse_detail(self,response):
        item = deepcopy(response.meta['item'])
        time = response.xpath("//div[@class='ctitle_spe']/div[1]/span[3]/text()").extract_first()
        if not time:
            time = response.xpath("//div[@class='ctitle_spe']/div[1]/span[2]/text()").extract_first()
        item['time'] = time
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='ctext']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['media'] = '手机中国'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        # m.update(str(item['url'])).encode('utf-8')
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        item['addr_province'] = '全国'
        # print(item)
        yield item

