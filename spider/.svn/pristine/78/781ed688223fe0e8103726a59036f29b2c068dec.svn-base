# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 阳泉新闻网爬虫 首页:
# =============================================================================


class YangquanxinwenwangSpider(scrapy.Spider):
    name = 'yangquanxinwenwang'
    allowed_domains = ['yqnews.com.cn']
    start_urls = ['http://www.yqnews.com.cn/']


    def parse(self, response):
        res = response.xpath('/html/body/table[10]/tr/td[1]/table/tr/td[1]/a/@href|\
        /html/body/table[10]/tr/td[3]/table/tr/td[1]/a/@href\
        |/html/body/table[12]/tr/td[3]/table/tr/td/table/tr/td[2]/a/@href\
        |/html/body/table[12]/tr/td[3]/table/tr/td/table/tr[1]/td[3]/a/@href').extract()
        for url in res:
            url = 'http://www.yqnews.com.cn/' + url.replace('./', '')
            yield scrapy.Request(url, callback=self.get_detail_url,meta={'url':url})


    def get_detail_url(self,response):
        res = response.body.decode()
        data = re.findall(r'32px;" href="(.*?)" class="bt_link"',res)
        for url in data:
            if 'http' not in url:
                url = response.url+url.replace('./', '')
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

        for i in range(1,3):
            url= response.url +'index_{}.html'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url1, meta={'url':response.meta['url']})

    def get_detail_url1(self, response):
        res = response.body.decode()
        data = re.findall(r'32px;" href="(.*?)" class="bt_link"',res)
        for url in data:
            if 'http' not in url:
                url = response.meta['url']+url.replace('./', '')
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('/html/body/table[4]/tr[2]/td/table/tr[2]/td|//*[@id="activity-name"]').xpath('string(.)').extract_first()
        item['time'] = response.xpath('/html/body/table[4]/tr[5]/td[1]/table/tr/td/text()|//*[@id="publish_time"]/text()').extract()
        item['content'] = response.xpath('//div[@class="TRS_Editor"]/p|//td[@class="bt_content"]/p|//*[@id="ozoom"]/p').xpath('string(.)').extract()
        item['come_from'] = response.xpath('/html/body/table[4]/tr[5]/td[2]/table/tr/td|//*[@id="js_name"]').xpath('string(.)').extract_first()
        if  item['title'] and item['content']:
            item['title'] = item['title'].split('\n')[1]
            try:
                item['time'] = item['time'][0].split('发布日期：')[1]
            except:
                try:
                    item['time'] = item['time'].replace('年','/').replace('月','/').replace('日','')
                except:
                    pass
            item['come_from']= item['come_from'].split('来源：')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()

            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '阳泉新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_city'] = '阳泉'
            item['addr_province'] = '山西省'
            print('阳泉新闻网' * 100)
            yield item




