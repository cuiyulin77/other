# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


class YandongewangSpider(scrapy.Spider):
    name = 'yandongewang'
    allowed_domains = ['bxgdw']
    start_urls = ['http://www.bxgdw.com/xw/index.shtml']
    custom_settings = {'DOWNLOAD_DELAY': 0.7}

    def parse(self, response):
        res  = response.xpath('//div/div[position()<20]/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()
        item['title'] = response.xpath('//tr[2]/td/text()').extract_first()
        item['time'] = response.xpath('//tr[4]/td/div/text()').extract_first()
        item['content'] = response.xpath('//tr[7]/td/div/text()').extract()
        item['come_from'] = response.xpath("//tr[4]/td/div/text()").extract_first()
        if item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split('\xa0\xa0\xa0\xa0')[1].split('\xa0')[1]
            item['come_from'] = item['come_from'].split('\xa0\xa0\xa0\xa0')[1].split('\xa0')[0].split('稿源：')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '燕东e网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '本溪'
            yield item
