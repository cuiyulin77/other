# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import re
import hashlib
import datetime

#======================================================================================
# 辽阳市政府爬虫http://www.liaoyang.gov.cn
#======================================================================================

class ChaoyanSpider(scrapy.Spider):
    name = 'chaoyan'
    allowed_domains = ['liaoyang']
    start_urls = ['http://www.liaoyang.gov.cn/lyszf/index.html',]
    custom_settings = {'DOWNLOAD_DELAY': 0.02}
    a = []

    def parse(self, response):
        res = response.xpath('//div[@class="tabk"]/a/@href').extract()
        for url in res:
            url1 = 'http://www.liaoyang.gov.cn'+url
            yield scrapy.Request(url1,callback=self.get_detail_url,dont_filter=True,meta={'item':url})
    def get_detail_url(self,response):
        # print(response.body.decode())
        node = response.meta['item']
        res = re.findall(r'<li><i></i><a href="(.*?)" target="_blank">',response.body.decode())
        for url in res:
            url = 'http://www.liaoyang.gov.cn'+url
            # print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
        for i in range(1,30):
            node = node.split('glist.html')[0]
            url = 'http://www.liaoyang.gov.cn'+node+'glist{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url_list, dont_filter=True)
    def get_detail_url_list(self,response):
        res = re.findall(r'<li><i></i><a href="(.*?)" target="_blank">',response.body.decode())
        for url in res:
            url = 'http://www.liaoyang.gov.cn'+url
            # print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)



    def  get_detail(self,response):
        item= SomenewItem()
        con = response.body.decode()
        item['title']= re.findall(r'<div class="bt">\s+(.*)\r\s+</div>',con)[0]
        item['time'] = response.xpath('//div[@class="time"]/div[1]/text()').extract_first()
        item['content'] = response.xpath('//*[@id="zoom"]/p/span/text()|//*[@id="zoom"]/span/text()|//*[@id="zoom"]/p/*/text()|//*[@id="zoom"]/p[1]/text/text()|//div[@class="nei"]/p/text()').extract()
        item['come_from'] = re.findall('来源:(.*)\r\s+</div>',con)[0].strip()

        if item['title'] and item['content'] and item['time']:
            item['time']= item['time'].split('来源')[0].split('发布时间:')[1].strip()
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '辽阳市政府'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            item['addr_city'] = '辽阳市'
            # print(item)
            yield item
            # print('辽阳市政府' * 100)



