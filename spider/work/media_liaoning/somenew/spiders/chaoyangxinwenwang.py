# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime

#======================================================================================
# 朝阳新闻网爬虫http://chaoyang.nen.com.cn
#======================================================================================

class ChaoyangxinwenwangSpider(scrapy.Spider):
    name = 'chaoyangxinwenwang'
    allowed_domains = ['chaoyang.nen.com']
    start_urls = ['http://chaoyang.nen.com.cn/xwdt/cyyw.asp','http://chaoyang.nen.com.cn/xwdt/ywmt.asp'\
        ,'http://chaoyang.nen.com.cn/xwdt/shxw.asp','http://chaoyang.nen.com.cn/xwdt/hyxw.asp'\
        ,'http://chaoyang.nen.com.cn/xwdt/xqxw.asp','http://chaoyang.nen.com.cn/xwdt/ztbd.asp']

    def parse(self, response):
        res = response.xpath('/html/body/table[6]/tr[2]/td/table/tr/td[1]/table/tr[3]/td/table[2]/tr/td/span/a/@href').extract()
        for url in res:
            url = 'http://chaoyang.nen.com.cn'+ url.strip()
            # print(url)
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)

    def get_detail(self,response):
        print(response.url)
        item= SomenewItem()
        item['title']= response.xpath('/html/body/table[6]/tr[2]/td/table/tr/td[1]/table/tr[3]/td/table/tr[1]/td/div/h2/text()').extract_first()
        item['time'] = response.xpath('/html/body/table[6]/tr[2]/td/table/tr/td[1]/table/tr[3]/td/table/tr[2]/td/span/text()').extract_first()
        item['content'] = response.xpath('//*[@id="Zoom"]/span/text()|//*[@id="Zoom"]/p/span/text()').extract()
        item['come_from'] = response.xpath('/html/body/table[6]/tr[2]/td/table/tr/td[1]/table/tr[3]/td/table/tr[2]/td/span/text()').extract_first()
        if item['title'] and item['content'] and item['time']:
            item['time'] = item['time'].split('\u3000\u3000')[2].split('发表日期：')[1]
            item['come_from']= item['come_from'].split('\u3000\u3000')[1].split('来源：')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '朝阳新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            item['addr_city'] = '朝阳市'
            # print(item)
            yield item


