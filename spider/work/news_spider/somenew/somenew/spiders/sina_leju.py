# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
import datetime
import time
from copy import deepcopy
import hashlib
from somenew.items import SomenewItem

class SinaLejuSpider(scrapy.Spider):
    name = 'sina_leju'
    allowed_domains = ['news.leju.com']
    start_urls = ['http://www.leju.com/']

    def parse(self, response):
        url_list = []
        for i in range(500)[1:]:

            # 获取json的url地址，地址格式如下，但是url地址中的'{'和'}'，会导致keyErro错误，吧url地址中的{换成‘%7B’，'}'换成'%7D',才能不报错
            # http://info.leju.com/search/default/index?type=new_news&ver=2.0&appid=2017062081&count=1&field=title|tags|url|photo_manage|media|topcolumn|createtime|zhaiyao&pcount=10&page=2&order={createtime}desc&format=jsonp&filter3={id@neq}6399038048314899569|6399036993782988778|6399042246326665090|6399036280185077176|6399039908396448996|6399038881207205020&filter0={deleted@eq}0&filter1={city@eq}bj&filter2={topcolumn@eq}%E6%95%B0%E6%8D%AE|%E6%94%BF%E7%AD%96|%E5%9C%9F%E5%9C%B0|%E5%85%AC%E5%8F%B8|%E4%BA%BA%E7%89%A9|%E5%9C%B0%E4%BA%A7K%E7%BA%BF|%E5%9C%B0%E4%BA%A7%E6%9C%AD%E8%AE%B0|%E8%A7%81%E5%9C%B0&callback=jQuery112403131369836538447_1525685228378&_=1525685228384
            url = 'http://info.leju.com/search/default/index?type=new_news&ver=2.0&appid=2017062081&count=1&field=title|tags|url|photo_manage|media|topcolumn|createtime|zhaiyao&pcount=10&page={}&order=%7Bcreatetime%7Ddesc&format=jsonp&filter3=%7Bid@neq%7D6399038048314899569|6399036993782988778|6399042246326665090|6399036280185077176|6399039908396448996|6399038881207205020&filter0=%7Bdeleted@eq%7D0&filter1=%7Bcity@eq%7Dfangnews'.format(i)
            url_list.append(url)
        # print('1'*50)
        # print(url_list)
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_get_ret,dont_filter=True)

    def parse_get_ret(self, response):
        ret = response.body.decode()
        # print("2"*30)
        res = ret.replace("(",'').replace(")",'')
        dict = json.loads(res)
        content_list = dict['data']
        for content in content_list:
            item = SomenewItem()
            # 获取新闻标题
            item['title'] = content['title']
            # 获取新闻的url
            item['url'] = content['url']
            item['media'] = content['media']
            # 获取ctime时间戳
            item['time'] = content['createtime']
            # 转换为正常时间
            time_local = time.localtime(int(item['time']))
            item['time'] = time.strftime("%Y/%m/%d %H:%M:%S", time_local)
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = deepcopy(response.meta['item'])
        # 获取内容
        content = response.xpath("//div[@class='article-body']")
        item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ' ')

        # 创建时间
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        # m.update(str(item['url'])).encode('utf-8')
        item['article_id'] = article_id
        yield item
