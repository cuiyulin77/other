# -*- coding: utf-8 -*-
import scrapy
import hashlib
import json
from somenew.items import SomenewItem
from copy import deepcopy
import datetime

# 法制（nid=113207），时政(nid=113352),地方(nid=113321),财经首页(nid=11147664),财经财眼(nid=115093),财发现(nid=1151357),
# 新华军网中国频道(nid=11139635),新华军网世界频道(nid=11139636),新华军网观点(nid=11139637),
# 新华军网要闻(nid=11139631),新华军网专题（nid=11139632）,新华军网锐读(nid=11139638),新华军网阅军情(nid=11139634),新华军网国防动员(nid=11139639)，
# 新华军网军民融合(nid=11139640)，新华军网航天防务(nid=11139641)，新华军网边防(nid=11139642),军医(nid=11139643),
# http://qc.wa.news.cn/nodeart/list?nid=11139636&pgnum=2&cnt=15&tp=1&orderby=1?
# ['113207', '113352', '113321', '11147664', '115093', '1151357', '11139635', '11139636', '11139637', '11139631', '11139632', '11139638', '11139634', '11139639', '11139640', '11139641', '11139642', '11139643']
# http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=2&cnt=10&tp=1&orderby=1?
# 爬取新华网相关新闻
class XinhuaSpider(scrapy.Spider):
    name = 'xinhua'
    allowed_domains = ['xinhuanet.com','qc.wa.news.cn']
    start_urls = ['http://xinhuanet.com/']

    xinhua_nid = ['113207', '113352', '113321', '11147664', '115093', '1151357', '11139635', '11139636', '11139637', '11139631', '11139632', '11139638', '11139634', '11139639', '11139640', '11139641', '11139642', '11139643']
    url_list = []
    for i in range(100):
        for nid in xinhua_nid:
            url = 'http://qc.wa.news.cn/nodeart/list?nid='+nid+'&pgnum='+str(i)+'&cnt=10&tp=1&orderby=1?'
            url_list.append(url)


    def parse(self, response):
        for url in self.url_list:
            yield scrapy.Request(url,self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        res_str = response.body.decode()
        ret = res_str.replace("(", '').replace(")", '')
        dict = json.loads(ret)
        print(dict)
        content_list = dict['data']['list']
        for content in content_list:
            item = SomenewItem()
            item['title'] = content['Title']
            item['url'] = content['LinkUrl']
            item['time'] = content['PubTime']
            item['media'] = content['SourceName']
            yield scrapy.Request(item['url'],callback=self.get_content,meta={'item':deepcopy(item)},dont_filter=True)

    def get_content(self,response):
        item = response.meta['item']
        content = response.xpath("//div[@id='p-detail']")
        item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace("\r", "")
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        print(item)
        yield item






