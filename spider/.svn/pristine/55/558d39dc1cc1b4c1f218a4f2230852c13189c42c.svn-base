# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
import re
from somenew.utils.get_start_urls import get_urls

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com','m.weibo.cn']
    # urls = get_urls("微博")
    start_urls = ['m.weibo.cn']
    custom_settings = {
        # 'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {'somenew.pipelines.DBPipeline': 30},
        'DOWNLOADER_MIDDLEWARES': {
            'somenew.middlewares.RandomUserAgent': 1,
            'somenew.middlewares.RandomProxy': 100,
        }
    }

    def start_requests(self):
        urls = get_urls("微博")
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        item = SomenewItem()
        html = response.body.decode()
        comm_num_re = re.search('\"comments_count\"\: (\d+)', html, re.S)
        if comm_num_re:
            item['comm_num'] = comm_num_re.group(1)
        else:
            item['comm_num'] = 0
        env_num_re = re.search('\"reposts_count\"\: (\d+)',html,re.S)
        if env_num_re:
            item['env_num'] = env_num_re.group(1)
        else:
            item['env_num'] = 0
        fav_num_re = re.search('\"attitudes_count\"\: (\d+)',html,re.S)
        if fav_num_re:
            item['fav_num'] = fav_num_re.group(1)
        else:
            item['fav_num'] = 0
        item['read_num'] = 0
        item['hot_value'] = int(item['comm_num'])+int(item['env_num'])+int(item['fav_num'])
        item['article_id'] = get_md5(response.url)
        yield item























