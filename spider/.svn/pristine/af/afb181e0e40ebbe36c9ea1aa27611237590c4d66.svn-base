# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
from somenew.utils.get_start_urls import get_urls
from somenew.utils.common import get_md5
from copy import deepcopy
import json


class HuanqiuSpider(scrapy.Spider):
    name = 'huanqiu'
    allowed_domains = ['huanqiu.com']
    # urls = get_urls("环球网")
    # print(urls)
    start_urls = ['huanqiu.com']

    def start_requests(self):
        urls = get_urls("环球网")
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        item = SomenewItem()
        url = str(response.url)
        title = response.xpath("//div[@class='l_a']/h1/text()").extract_first()
        item['article_id'] = get_md5(url)
        sourceid = response.xpath("//meta[@name='contentid']/@content").extract_first()
        com_url = 'https://commentn.huanqiu.com/api/v2/async?a=comment&m=source_info&appid=e8fcff106c8f&sourceid=' + sourceid + '&url=' + \
                  url + '&title=' + title
        yield scrapy.Request(com_url, callback=self.get_com_num, meta={'item': item})

    def get_com_num(self, response):
        item = deepcopy(response.meta['item'])
        ret = response.body.decode()
        dict = json.loads(ret)
        if dict['msg'] == 'success':
            n_comment = dict['data']['n_comment']
            n_active = dict['data']['n_active']
            item['comm_num'] = int(n_comment) + int(n_active)
        else:
            item['comm_num'] = '0'
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['hot_value'] = item['comm_num']
        # print(item)
        yield item






