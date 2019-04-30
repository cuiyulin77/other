# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json


# =============================================================================
# 临汾新闻网爬虫 首页:
# ===========================================================================


class LinfenxinwenwangSpider(scrapy.Spider):
    name = 'linfenxinwenwang'
    allowed_domains = ['lfxww.com']
    start_urls = ['http://www.lfxww.com/shanxi/','http://www.lfxww.com/linfen/shizheng/',\
                  'http://www.lfxww.com/linfen/xnc/','http://www.lfxww.com/linfen/fzsh/',\
                  'http://www.lfxww.com/linfen/kjww/','http://www.lfxww.com/linfen/glps/',\
                  'http://www.lfxww.com/linfen/djll/','http://www.lfxww.com/linfen/pyrw/','http://www.lfxww.com/linfen/ft/']


    def parse(self, response):
        print(len(response.url), response.url)
        res = response.xpath('//*[@id="contentText"]/div/ul/li/a/@href').extract()
        for url in res:
            if 'h5' not in url:
                yield scrapy.Request(url, callback=self.get_detail)

        for i in range(1,5):
            url = response.url +'index_{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url,meta={'url':response.url})

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="contentText"]/div/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self, response):
        item = SomenewItem()
        print(response.url, '我是响应的rul')
        item['title'] = response.xpath('/html/body/div[3]/div/div/div[1]/h2/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[3]/div/div/div[1]/h3/text()').extract()[0]
        item['content'] = response.xpath('//div[@class="col-md-12 nry jcontent"]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('/html/body/div[3]/div/div/div[1]/h3/text()').extract()[0]
        if item['title'] and item['content']:
            item['time'] = item['time'].split('来源：')[0]
            item['url'] = response.url
            item['come_from'] =  item['come_from'].split('来源：')[1].split('\u3000\u3000')[0]
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                             '').replace(
                '\u2002', '').replace('\t', '').replace('\r', '').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '临汾新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '临汾'
            item['addr_province'] = '山西省'
            print('临汾新闻网' * 100)
            yield item


