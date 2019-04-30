# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
import hashlib
import datetime
import time
import json

# =============================================================================
# 新浪山西爬虫 首页:
# =============================================================================


class XinlangliaoningSpider(scrapy.Spider):
    name = 'xinlangshanxi'
    allowed_domains = ['sina']
    start_urls = (
        'http://shanxi.sina.cn/news/ty/list-p1.d.html?vt=4',
    )

    def parse(self, response):
        print(response.url)
        ret = response.body.decode()
        res1 = re.findall(r'<a href="(.*?)" data-cid=', ret)
        for url in res1:
            yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
        for i in range(1,34):
            url ='http://interface.sina.cn/dfz/outside/wap/news/list.d.html?col=56323&level=undefined&show_num=15&page={}&act=more&jsoncallback=callbackFunction&callback=jsonp1'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get_detail_url(self,response):
        print(response.url)
        print(response.body.decode())
        res = re.findall(r'callbackFunction\((.*)\)',response.body.decode())
        ret = json.loads(res[0])
        ret_list = ret['result']['data']['list']
        for data in ret_list:
            url = data['URL']
            print(url, '我是提取的url')
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
    def get_detail(self, response):
        item = SomenewItem()
        print(response.url,'我是响应的rul')
        item['title'] = response.xpath('/html/body/main/section[1]/article/h1/text()').extract_first()
        item['time'] = response.xpath('//time[@class="weibo_time"]|/html/body/main/section[1]/article/time').xpath('string(.)').extract_first()
        item['content'] = response.xpath('/html/body/main/section[1]/article/p/text()').extract()
        item['come_from'] = response.xpath('/html/body/main/section[1]/article/section[1]/figure/figcaption/h2/text()').extract_first()
        if  item['title'] and item['content'] and item['time']:
            item['time']= item['time'].split('\t')
            if len(item['time']) != 1:
                item['time']= item['time'][6]+' '+item['time'][12]
                localtime = time.asctime(time.localtime(time.time()))
                item['time'] = localtime.split()[-1]+'/'+item['time']
                item['time'] = item['time'].replace('月','/').replace('日','')
            else:
                c  = item['time'][0]
                a = re.findall(r'[^\u4e00-\u9fa5]',c)
                b = ''
                for i in range(len(a)):
                    b = b +a[i]
                item['time'] = b
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '新浪山西'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            # item['addr_city'] = None
            item['addr_province'] = '山西省'
            print('山西新闻网' * 100)
            yield item


