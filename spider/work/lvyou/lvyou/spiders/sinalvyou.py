# -*- coding: utf-8 -*-
#=============================================================================
# 新浪旅游爬虫,直接插入新评网的数据库
# =============================================================================

import scrapy
from lvyou.items import LvyouItem
from lvyou.utils.common import get_md5
import hashlib
import datetime
import time
import json


class SinalvyouSpider(scrapy.Spider):
    name = 'sinalvyou'
    allowed_domains = ['sina.cn', ]
    start_urls = ['http://travel.sina.cn/interface/2018_feed.d.json?page=1&type=hot']
    url_list = []
    for i in range(2, 20):
        url = 'http://travel.sina.cn/interface/2018_feed.d.json?page={}&type=hot'.format(i)
        print(url)
        url_list.append(url)
    start_urls = url_list

    def parse(self, response):
        # print(response.url)
        ret = response.text
        res = json.loads(ret)['cards']
        # print(res)
        for i in res:
            item = LvyouItem()
            item['titlepic'] = 'http:' + i['pic']
            url = 'http:' + i['scheme']
            # url ='http://travel.sina.com.cn/outbound/pages/2019-01-07/detail-ihqfskcn4730144.shtml'
            yield scrapy.Request(url, callback=self.get_detail, meta={'item': item}, dont_filter=True)

    def get_detail(self, response):
        item = response.meta['item']
        # print(response.url,'我是响应的rul')
        item['title'] = response.xpath('//*[@id="artibodyTitle"]/text()').extract_first()
        item['newstime'] = response.xpath('//*[@id="wrapOuter"]/div/div[2]/span/text()').extract()
        item['newstime'] = " ".join(item['newstime'])
        item['writer'] = response.xpath('//*[@id="wrapOuter"]/div/div[2]/span/span/a/text()').extract_first()
        # a  = re.findall('charset:\'GBK\'}\);(.*)id="relatedNewsWrap"',response.body.decode(),re.S)[0]
        # a = re.findall(r' charset:\'GBK\'});\n</script>(.*)id="relatedNewsWrap"', response.body.decode(), re.S)[0]
        content = response.xpath("//div[@id='artibody']").extract()
        item['content'] = ''.join(content).replace('\u3000', '&nbsp;').replace('\xa0', '&nbsp;')
        item['classid'] = '52'
        item['newstime'] = item['newstime'].split('\n')[1].strip().replace('年', '-').replace('月', '-').replace('日', ' ')
        timeArray = time.strptime(item['newstime'], "%Y-%m-%d %H:%M")
        item['newstime'] = int(time.mktime(timeArray))
        item['url'] = response.url
        item['article_id'] = get_md5(item['url'])
        item['keyid'] = ' '
        item['media'] = '新浪网'
        # print(item)
        yield item