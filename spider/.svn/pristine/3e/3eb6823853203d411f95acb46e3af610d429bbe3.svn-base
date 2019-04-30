# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
from somenew.utils.get_start_urls import get_urls
import json
from copy import deepcopy

# ============================================
# 新浪山西,新浪辽宁 hot_value爬虫
# ============================================

class XinlangshanxiSpider(scrapy.Spider):
    name = 'xinlangshanxi'
    allowed_domains = ['sina.cn']
    start_urls = ['sina.cn']
    custom_settings = {
        # 'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {'somenew.pipelines.DBPipeline': 30},
        'DOWNLOADER_MIDDLEWARES': {
            'somenew.middlewares.RandomUserAgent': 1,
            'somenew.middlewares.RandomProxy': 100,
        }
    }

    def start_requests(self):
        # urls1 = get_urls("新浪山西")
        # urls2 = get_urls('新浪辽宁')
        # urls = urls1 + urls2
        urls = ['http://ln.sina.cn/news/2019-03-14/detail-ihrfqzkc3857060.d.html?vt=4&cid=56316',
                'http://ln.sina.cn/news/2019-03-14/detail-ihsxncvh2485639.d.html?vt=4&cid=56316',
                'http://ln.sina.cn/news/2019-03-14/detail-ihsxncvh2485426.d.html?vt=4&cid=56316',
                'http://ln.sina.cn/news/2019-03-14/detail-ihsxncvh2354400.d.html'
                ]

        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        content = re.search("getcomments:'(.*?)'",response.text,re.S)
        url = content.group(1)
        comment_url = 'http:'+url
        item = SomenewItem()
        item['article_id'] = get_md5(response.url)
        yield scrapy.Request(comment_url,callback=self.get_comment_num,meta={'item':item})

    def get_comment_num(self,response):
        item = deepcopy(response.meta['item'])
        text_str = json.loads(response.text)
        try:
            item['comm_num'] = text_str.get('data',0).get('cmnt',0).get('total',0)
        except:
            item['comm_num'] = 0
        item['read_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['hot_value'] = item['comm_num']
        # print(item)
        yield item

