# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 新华报业
    name = 'xinhuabaoye'
    allowed_domains = ['news.xhby.net']
    start_urls = ['http://news.xhby.net/guonei/','http://news.xhby.net/jj/gongs/',\
                  'http://news.xhby.net/jj/yw/','http://js.xhby.net/jj/',\
                  'http://news.xhby.net/shehui/sj/','http://news.xhby.net/jj/hgjj/',\
                  'http://news.xhby.net/gj/','http://news.xhby.net/ty/',\
                  'http://news.xhby.net/shehui/fz/','http://news.xhby.net/guonei/gn/',\
                  'http://news.xhby.net/shehui/rd/','http://js.xhby.net/sz/',\
                  'http://js.xhby.net/zx/','http://js.xhby.net/jj/',\
                  'http://js.xhby.net/kjyw/','http://js.xhby.net/ylws/','http://js.xhby.net/ylws/']
    def parse(self, response):
        res = response.xpath('//*[@id="list14"]/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"title\"]/text()").extract_first()
        item['come_from'] = response.xpath("//*[@id=\"source_baidu\"]/a/text()|//*[@id=\"source_baidu\"]/text()").extract()
        item['content'] = response.xpath('//*[@id="content"]/p/text()|//*[@id="content"]/*/p/text()').extract()
        try:
            item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()|//*[@id=\"content-source\"]/date/text()").extract()[0]
        except:
            item['time'] = ''
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        # print(item)
        if item['content'] and item['title']:
            item['come_from'] = ''.join(item['come_from']).replace('\r\n', '').replace('来源： ',' ').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '新华报业'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江苏'
            print(item)
            yield item


