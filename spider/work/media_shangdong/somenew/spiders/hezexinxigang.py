# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem

class HezexinxigangSpider(scrapy.Spider):
    name = 'hezexinxigang'
    allowed_domains = ['heze.cc']
    start_urls = ['http://www.heze.cc/']

    def parse(self, response):
        res = response.xpath('//*[@id="bfxz_con_1"]/a/@href').extract()
        for url in res:
            print(url,'发送请求的url')
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)


    def get_detail(self,response):
        item = SomenewItem()
        print(response.url,'响应url')
        item['content'] = response.xpath('//*[@id="zoom"]/p/text()').extract()
        item['title'] = response.xpath('/html/body/div/table/tr/td/table/tr[3]/td[2]/table[1]/tr[1]/td/text()|//*[@id="thread_subject"]/text()').extract()
        item['time'] = response.xpath('/html/body/div/table/tr/td/table/tr[3]/td[2]/table[2]/tr/td/table/tr/td[1]/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            item['title'] = ''.join(item['title']).replace('\n','').replace('\t','').replace('\u3000','').replace('\r','')
            item['content'] = ''.join(item['content']).replace('\u3000','').replace('\ufeff','').replace('\xa0','')
            item['time'] = item['time'].split('发布时间：')[1]
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '菏泽在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] ='菏泽政府网'
            item['addr_province'] = '山东省'
            item['addr_city'] = '菏泽'
            yield item