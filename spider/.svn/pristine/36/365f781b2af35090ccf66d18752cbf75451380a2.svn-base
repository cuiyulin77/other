# -*- coding: utf-8 -*-

import scrapy
import re
import json
from somenew.utils.common import get_md5
from copy import deepcopy
from somenew.items import SomenewItem
from somenew.utils.get_start_urls import get_urls

class QqnewsSpider(scrapy.Spider):
    name = 'qqnews'
    allowed_domains = ['qq.com']
    # urls = get_urls("腾讯新闻")
    # print(urls)
    start_urls = ['qq.com']

    def start_requests(self):
        urls = get_urls("腾讯新闻")
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        item = SomenewItem()
        url = response.url
        item['article_id'] = get_md5(url)
        # if not item['content'] == '':
        html = response.xpath("//*[@id='Main-Article-QQ']/div/div[1]/div[2]/script/text()").extract_first()
        # 如果没有取到cmt_id,说明comm_num=0
        if html:
            html = html.replace("\n",'').replace(' ','')
            cmt_id = re.match('.*?cmt_id=(\d+).*', html).group(1)
            com_url = 'https://coral.qq.com/article/' + cmt_id + '/commentnum'
            yield scrapy.Request(com_url, callback=self.get_comm_num, dont_filter=True, meta={'item': item})
        else:
            item['comm_num'] = 0
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['hot_value'] = 0
            yield item

    def get_comm_num(self, response):
        item = deepcopy(response.meta['item'])
        html = response.body.decode()
        dic = json.loads(html)
        item['comm_num'] = dic['data']['commentnum']
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['hot_value'] = item['comm_num']
        yield item




