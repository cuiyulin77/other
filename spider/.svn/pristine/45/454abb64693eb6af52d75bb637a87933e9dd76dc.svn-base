# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 中国新闻网江苏
    name = 'zhongwangxinwenwngjiangsu'
    allowed_domains = ['chinanews.com']
    start_urls = ['http://www.js.chinanews.com/business/','http://www.js.chinanews.com/house/','http://www.js.chinanews.com/highlights/','http://www.js.chinanews.com/citynews/','http://www.js.chinanews.com/nomocracy/','http://www.js.chinanews.com/science/','http://www.js.chinanews.com/sports/']
    def parse(self, response):
        res = response.xpath('//*[@id="list"]/ul/li/a/@href').extract()
        for url in res:
            url  = 'http://www.js.chinanews.com'+url
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="content"]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"cont\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"time\"]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="txt"]/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id=\"come\"]/text()").extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '中国新闻网江苏'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['addr_province'] = '江苏'
            yield item


