# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 新京报
    name = 'xinjingbao'
    allowed_domains = ['bjnews.com.cn']
    start_urls =['http://www.bjnews.com.cn/realtime','http://www.bjnews.com.cn/opinion/','http://www.bjnews.com.cn/book/',\
                 'http://www.bjnews.com.cn/invest/','http://www.bjnews.com.cn/roll','http://www.bjnews.com.cn/feature',\
                 'http://www.bjnews.com.cn/inside','http://www.bjnews.com.cn/finance/','http://www.bjnews.com.cn/culture/',\
                 'http://www.bjnews.com.cn/auto/','http://www.bjnews.com.cn/home/','http://www.bjnews.com.cn/fashion/',\
                 'http://www.bjnews.com.cn/travel/','http://www.bjnews.com.cn/food/','http://www.bjnews.com.cn/health/',\
                 'http://www.bjnews.com.cn/video/','http://www.bjnews.com.cn/sport/,''http://www.bjnews.com.cn/news/',\
                 'http://www.bjnews.com.cn/world/','http://www.bjnews.com.cn/ent/','http://www.bjnews.com.cn/house/']

    def parse(self, response):
        res = response.xpath('//*[@id="news_ul"]/li/a/@href|//*[@id="news_ul"]/li/div/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['time'] = response.xpath("//div[@class=\"fl ntit_l\"]/span[1]/text()").extract_first()
        item['title']  = response.xpath("//div[@class=\"title\"]/h1/text()").extract_first()
        item['content'] = response.xpath('//div[@class="content"]/p/text()').extract()
        a = ''
        for i in item['content']:
            i= i.replace('\xa0',' ').replace('\u3000\u3000',' ')
            a += i
        item['content'] = a
        print(item['content'],item['time'],item['title'])
        if item['content'] and item['time'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '新京报'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = '新京报'
            item['addr_province'] = '北京'
            item['addr_city'] ='北京'
            yield item


