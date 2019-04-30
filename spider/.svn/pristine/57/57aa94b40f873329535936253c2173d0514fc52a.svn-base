# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
from somenew.utils.get_start_urls import get_urls
import json
from copy import deepcopy
# ============================================
# 新京报 hot_value爬虫
# ============================================

class XinjingbaoSpider(scrapy.Spider):
    name = 'xinjingbao'
    allowed_domains = ['bjnews.com.cn']
    start_urls = ['http://bjnews.com.cn/']
    custom_settings = {
        # 'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {'somenew.pipelines.DBPipeline': 30},
        'DOWNLOADER_MIDDLEWARES': {
            'somenew.middlewares.RandomUserAgent': 1,
            # 'somenew.middlewares.RandomProxy': 100,
        }
    }

    def start_requests(self):
        # urls = get_urls("新京报")
        urls = ['http://www.bjnews.com.cn/news/2019/03/14/555998.html',
                'http://www.bjnews.com.cn/news/2019/03/14/556050.html',
                'http://www.bjnews.com.cn/news/2019/03/14/556041.html',
                'http://www.bjnews.com.cn/world/2019/03/14/556018.html'
                ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        id = response.xpath("//div[@class='attitude']/span/@data-id").extract_first()
        upnum_url = 'http://www.bjnews.com.cn/webapi/getupnum?id='+str(id)
        item = SomenewItem()
        item['article_id'] = get_md5(response.url)
        yield scrapy.Request(upnum_url, callback=self.get_comment_num, meta={'item': item})

    def get_comment_num(self,response):
        # http://www.bjnews.com.cn/webapi/getupnum?id=555998
        item = deepcopy(response.meta['item'])
        text_str = json.loads(response.text)
        item['comm_num'] = 0
        item['read_num'] = 0
        item['fav_num'] = text_str.get('upnum', 0)
        item['env_num'] = 0
        item['hot_value'] = item['fav_num']
        # print(item)
        yield item



