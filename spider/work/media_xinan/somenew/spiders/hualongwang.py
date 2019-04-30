# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime
import  re

class DezhouxinwenSpider(scrapy.Spider):
    # 华龙网
    name = 'hualongwang'
    allowed_domains = ['cqnews.net']
    start_urls = ['http://cq.cqnews.net/cqqx/html/col204351.htm','http://cq.cqnews.net/cqqx/col417130.htm',\
                  'http://tour.cqnews.net/html/col383605.htm','http://tour.cqnews.net/html/col383608.htm',\
                  'http://baby.cqnews.net/col220087.htm','http://health.cqnews.net/html/node_84160.htm',\
                  'http://health.cqnews.net/html/node_243147.htm','http://life.cqnews.net/html/col325950.htm',\
                  'http://car.cqnews.net/html/col84148.htm','http://car.cqnews.net/col123312.htm',\
                  'http://car.cqnews.net/col123312.htm','http://finance.cqnews.net/col24633.htm',\
                  'http://finance.cqnews.net/col30944.htm','http://finance.cqnews.net/col84177.htm',\
                  'http://3c.cqnews.net/col392096.htm','http://cq.cqnews.net/html/col35734.htm',\
                  'http://cq.cqnews.net/cqqx/html/col274243.htm','http://cq.cqnews.net/cqqx/html/col204350.htm',
                  'http://3c.cqnews.net/col392105.htm','http://3c.cqnews.net/col392100.htm']

    def parse(self, response):
        res = response.xpath('//div[@class="lb"]/ul[1]/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url,callback=self.get_detail)
            print(url)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"left_news\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"jiange3\"]/text()").extract_first()
        item['content'] = response.xpath('//*[@id="main_text"]/p/span/text()|//*[@id="main_text"]/p/text()').extract()
        item['come_from'] = '华龙网'
        # print(item)
        if item['content'] and item['time'] and item['title']:
            try:
                item['time'] = item['time'].split('\r\n')[1].strip()
            except:
                item['time'] = ''
            item['title'] = item['title'].split()[0]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '华龙网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '重庆'
            print(item)
            # yield item


