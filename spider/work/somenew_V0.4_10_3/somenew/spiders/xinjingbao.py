# -*- coding: utf-8 -*-
import scrapy
import json
from somenew.items import SomenewItem
from copy import deepcopy
import hashlib
import datetime

# 新京报爬虫
# 此爬虫是使用json获取url等信息，也可以在http://epaper.bjnews.com.cn/获取电子报的页面，从中获取报纸信息
class XinjingbaoSpider(scrapy.Spider):
    name = 'xinjingbao'
    allowed_domains = ['bjnews.com.cn']
    json_url_list = []
    for i in range(10)[1:]:
        url = 'http://www.bjnews.com.cn/webapi/hotlist?page=' + str(i) + '&t=0.32387063277519945'
        json_url_list.append(url)
    start_urls = json_url_list

    def parse(self, response):
        ret = response.body.decode()
        dict = json.loads(ret)
        data_list = dict['data']
        for data in data_list:
            item = SomenewItem()
            item['time'] = data['submit_time']
            item['title'] = data['title']
            item['url'] = response.urljoin(data['url'])
            yield scrapy.Request(item['url'], callback=self.get_content, meta={'item': deepcopy(item)})

    def get_content(self, response):
        item = response.meta['item']
        item['media'] = "新京报"
        item['content'] = response.xpath("//div[@class='content']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # 新京报没体现信息来源
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '报纸'
        item['addr_province'] = '北京'
        yield item
        # print(item)
