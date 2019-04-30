# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 中国江苏网
    name = 'zhonguojiangsuwang'
    allowed_domains = ['jschina.com.cn']
    start_urls = ['http://www.jschina.com.cn/']
    def parse(self, response):
        res = response.xpath('/html/body/div[14]/div[1]/div[2]/div/ul/li/a/@href|/html/body/div[20]/div[1]/div/ul/li/a/@href|/html/body/div[28]/div[3]/div[1]/ul/li/a/@href|/html/body/div[30]/div/div/a/@href|/html/body/div[30]/div/div/ul/li/a/@href|/html/body/div[32]/div/div/ul/li/a/@href|/html/body/div[34]/div[3]/div[1]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//*[@id=\"title\"]/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract()[0]
        item['content'] = response.xpath('//*[@id="zm"]/div/p/text()|//*[@id="content"]/div/p/text()').extract()
        item['come_from'] = response.xpath("//*[@id=\"source_baidu\"]/a/text()").extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        print(item)
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '中国江苏网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江苏'
            print(item)
            yield item