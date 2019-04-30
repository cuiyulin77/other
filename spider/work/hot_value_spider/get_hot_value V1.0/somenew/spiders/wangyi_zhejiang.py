# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
from somenew.utils.get_start_urls import get_urls
import json
from copy import deepcopy
# ============================================
# 网易hot_value爬虫,包括网易,网易浙江,网易辽宁
# ============================================

class WangyiZhejiangSpider(scrapy.Spider):
    name = 'wangyi_zhejiang'
    allowed_domains = ['163.com']
    start_urls = ['http://news.163.com/']
    custom_settings = {
        # 'DOWNLOAD_DELAY':3,
        'ITEM_PIPELINES':{'somenew.pipelines.DBPipeline': 30},
        'DOWNLOADER_MIDDLEWARES':{
            'somenew.middlewares.RandomUserAgent': 1,
            'somenew.middlewares.RandomProxy': 100,
        }
    }

    def start_requests(self):
        urls1 = get_urls("网易浙江")
        urls2 = get_urls('网易')
        urls3 = get_urls('网易辽宁')
        urls = urls1 + urls2 + urls3
        # urls = ['http://liaoning.news.163.com/19/0314/05/EA74TS1I04228EEJ.html',
        #         'http://liaoning.news.163.com/19/0314/05/EA73JUTS04228JCF.html',
        #         'http://liaoning.news.163.com/19/0314/09/EA7GTGNM04228EEJ.html'
        #         ]

        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        content = re.findall(r'("productKey".*)?"target"', response.text, re.S)
        content = ''.join(content).replace('\n', '').replace(' ', '')
        con =  "{"+content+"}"
        con = eval(con)          # {'productKey': 'a2869674571f77b5a0867c3d71db5856', 'docId': 'E9UT79BB0001875P'}
        item = SomenewItem()
        comment_url = 'https://comment.api.163.com/api/v1/products/{productKey}/threads/{docId}?ibc=jssdk'.format(productKey=con['productKey'],docId=con['docId'])
        item['article_id'] = get_md5(response.url)
        yield scrapy.Request(url=comment_url,callback=self.get_comment_num,meta={'item': item})

    def get_comment_num(self,response):
        item = deepcopy(response.meta['item'])
        text_str = json.loads(response.text)
        item['comm_num'] = text_str['cmtCount']
        item['read_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['hot_value'] = item['comm_num']
        # print(item)
        yield item

