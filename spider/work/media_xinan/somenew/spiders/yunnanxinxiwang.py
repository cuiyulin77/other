# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 云南信息刚
    name = 'yunnanxinxigang'
    allowed_domains = ['yninfo.com']
    start_urls =['http://travel.yninfo.com/news/','http://food.yninfo.com/news/','http://news.yninfo.com/','http://news.yninfo.com/yn/','http://news.yninfo.com/news_gd/index.html','http://news.yninfo.com/caijing/','http://ent.yninfo.com/','http://news.yninfo.com/tiyu/']

    def parse(self, response):
        res = response.xpath('//ul[@class="ync-list"]/li/h2/a/@href').extract()
        for url in res:
            url = 'http://news.yninfo.com/' +url.split('./')[1]
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
        for i in  range(1,20):
            url = 'http://news.yninfo.com/index_{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('//ul[@class="ync-list"]/li/h2/a/@href').extract()
        for url in res:
            url = 'http://news.yninfo.com/' +url.split('./')[1]
            yield scrapy.Request(url,callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"ync-content\"]/h2/text()").extract_first()
        item['time'] = response.xpath("//p[@class=\"time\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
        item['come_from'] = response.xpath("//p[@class=\"time\"]/text()").extract_first()
        if item['content'] and item['time'] and item['title']:
            item['time'] = item['time'].split()[0].replace('年', '/').replace('月', '/').replace('日', ' ')
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '云南信息港'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '云南'
            print(item)
            yield item


