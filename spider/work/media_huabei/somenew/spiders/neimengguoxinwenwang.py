# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 内蒙古新闻网
    name = 'neimengguoxinwenwang'
    allowed_domains = ['nmgnews.com.cn']
    start_urls =['http://inews.nmgnews.com.cn/sx/pl/index.shtml','http://inews.nmgnews.com.cn/nmgxw/shfzxw/',\
                 'http://gov.nmgnews.com.cn/lddt/index.shtml','http://gov.nmgnews.com.cn/szxw/index.shtml',\
                 'http://inews.nmgnews.com.cn/nmgxw/szxw/','http://economy.nmgnews.com.cn/lccp/',\
                 'http://economy.nmgnews.com.cn/yw/','http://economy.nmgnews.com.cn/qyfc/',\
                 'http://economy.nmgnews.com.cn/tzcy/','http://economy.nmgnews.com.cn/xyk/',\
                 'http://inews.nmgnews.com.cn/nmgxw/jjxw/','http://inews.nmgnews.com.cn/nmgxw/kjwwxw/',\
                 'http://china.nmgnews.com.cn/zh/index.shtml','http://inews.nmgnews.com.cn/nmgxw/nmqxm/',\
                 'http://inews.nmgnews.com.cn/nmgxw/shfzxw/','http://inews.nmgnews.com.cn/nmgxw/syxw/']


    def parse(self, response):
        res = response.xpath('//*[@id="div_left"]/table/tr/td[1]/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"div2\"]/text()").extract_first()
        item['time']  = response.xpath("//*[@id=\"div3\"]/span[1]/text()").extract_first().replace('19','2019')
        item['content'] = response.xpath('//*[@id="div_content"]/*//text()').extract()
        # print(item)
        a = ''
        for i in item['content']:
            i= i.replace('\xa0',' ').replace('\u3000\u3000',' ')
            a += i
        item['content'] = a
        # print(item['content'],item['time'],item['title'])
        if item['content'] and item['time'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '内蒙古新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = '内蒙古新闻网'
            item['addr_province'] = '内蒙古'
            yield item


