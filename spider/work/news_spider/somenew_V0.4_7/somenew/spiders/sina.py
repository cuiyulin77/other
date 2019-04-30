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

logger = logging.getLogger(__name__)

# 获取新浪的滚动新闻（并不是很全面，一些地方站没有爬取）
class SinanewSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        'http://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1',
    )

    def parse(self, response):
        url_list = []
        for i in range(15)[1:]:
            url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}&r=0.7356892603932603&callback=jQuery31109829711483500057_1525332319321&_=1525332319322'.format(i)
            url_list.append(url)
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_get_ret)

    def parse_get_ret(self, response):
        ret = response.body.decode()
        res = re.match('^try{\w*\((.*)\);}catch\(e\){};$',ret).group(1)
        dict = json.loads(res)
        content_list = dict['result']['data']
        for content in content_list:
            item = SomenewItem()
            # 获取新闻标题
            item['title'] = content['title']
            # 获取新闻的url
            item['url'] = content['url']
            item['media'] = "新浪网"
            # 获取ctime时间戳
            item['time'] = content['ctime']
            # 转换为正常时间
            time_local = time.localtime(int(item['time']))
            item['time'] = time.strftime("%Y/%m/%d %H:%M:%S",time_local)
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = deepcopy(response.meta['item'])
        # 获取内容
        item['content'] = response.xpath("//div[@class='article']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # 创建时间
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        # m.update(str(item['url'])).encode('utf-8')
        item['article_id'] = article_id
        yield item
