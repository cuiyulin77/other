# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 安徽在线
    name = 'anhuizaixian'
    allowed_domains = ['hf365.com']
    start_urls = ['http://www.hf365.com/hf365/news/bdyw/1.shtml','http://www.hf365.com/hf365/news/hfxw/hefeizx/','http://www.hf365.com/hf365/news/hfxw/wmkhf/','http://www.hf365.com/hf365/news/ahxw/ahxw/','http://www.hf365.com/hf365/news/hfxw/xqxw/','http://www.hf365.com/hf365/news/hfxw/sqxw/']
    def parse(self, response):
        res = response.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("/html/body/div[5]/div[1]/div[1]/h1/text()").extract_first()
        try:
            item['time'] = response.xpath("//span[@class=\"date\"]/text()").extract()[0]
        except:
            item['time'] = ''
        item['content'] = response.xpath('//div[@class="article-content clearfix"]/p/text()').extract()
        item['come_from'] = response.xpath("/html/body/div[5]/div[1]/div[1]/div[1]/span[3]/a/text()").extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '安徽在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江苏'
            yield item


