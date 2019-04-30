# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class HuanghexinwenwangSpider(scrapy.Spider):
    name = 'huanghexinwenwang'
    allowed_domains = ['sxgov.cn']
    start_urls = ['http://sx.sxgov.cn/node_142.htm','http://www.sxgov.cn/node_311.htm','http://www.sxgov.cn/node_292006.htm'\
        ,'http://www.sxgov.cn/node_292825.htm','http://law.sxgov.cn/node_3661.htm','http://law.sxgov.cn/node_23540.htm',\
                  'http://law.sxgov.cn/node_3665.htm','http://www.sxgov.cn/node_263.htm']

    def parse(self, response):
        print(len(response.url),response.url)
        res = response.xpath('//*[@id="conleft"]/div[2]/ul/li/a/@href').extract()
        for url in res:
            if 'http' not in url:
                url = response.url.split('node')[0]+url
                print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(2,10):
            url = response.url.replace('.htm','_{}.htm'.format(i))
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="conleft"]/div[2]/ul/li/a/@href').extract()
        for url in res:
            if 'http' not in url:
                url = response.url.split('node')[0] + url
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('//*[@id="conleft"]/div[1]/text()|//*[@id="title"]/h1/text()|//h1/text()|/html/body/table[7]/tbody/tr/td[1]/table[1]/tr/td/text()').extract_first()
        try:
            item['time'] = response.xpath('//*[@id="pubtime_baidu"]/text()|//*[@id="time"]/span/ul/li[1]').extract()[0]
        except:
            pass
        item['content'] = response.xpath('//*[@id="conleft"]/div/p/text()|//*[@id="ltext"]/p/text()|/html/body/div/div/div[2]/p/text()|//p/text()').extract()
        try:
            item['come_from'] = response.xpath('//*[@id="source_baidu"]/text()|//*[@id="time"]/span/ul/li[4]/text()').extract_first()
        except:
            pass

        if item['title'] and item['content']:
            item['title']= item['title'].split('\n')[1]
            try:
                item['come_from'] = item['come_from'].split('来源：')[1]
            except:
                pass
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '黄河新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '山西省'
            print('山西新闻网'*100)
            yield item





