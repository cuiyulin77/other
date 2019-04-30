# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re

class DezhouxinwenSpider(scrapy.Spider):
    # 福建网络电视台
    name = 'fujianwangluodianshitai'
    allowed_domains = ['fjtv.net']
    start_urls = ['http://media.fjtv.net/folder843/']
    def parse(self, response):
        for i in range(843,855):
            url = 'http://media.fjtv.net/folder{}/'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url)
        for i in range(819,829):
            url = 'http://society.fjtv.net/folder{}/'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url2)
    def get_detail_url(self,response):
        res = response.xpath('//div[@class="jieshao"]/p[1]/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail_url2(self,response):
        res = response.xpath('//div/div/p/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//div[@class=\"article-title\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"time\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="article-main"]/p/text()|//section/p/text()|//*[@id="playerDrag"]/div[3]/text()').extract()
        item['come_from'] = response.xpath("//span[@class=\"article-assist\"]/span[1]/text()|//span[@class=\"origin\"]/text()").extract_first()
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '福建网络电视台'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = item['come_from'].split('来源:')[1]
            item['addr_province'] = '福建'
            yield item



