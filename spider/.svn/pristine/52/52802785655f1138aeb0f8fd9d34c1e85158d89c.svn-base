# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
from somenew.utils.common import get_md5
from somenew.utils.get_start_urls import get_urls
import re


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    # urls = get_urls("今日头条")
    # print(urls)
    start_urls = ['toutiao.com']
    custom_settings = {
        # 'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {'somenew.pipelines.DBPipeline': 30},
        'DOWNLOADER_MIDDLEWARES': {
            'somenew.middlewares.RandomUserAgent': 1,
            'somenew.middlewares.RandomProxy': 100,
        }
    }

    def start_requests(self):
        urls = get_urls("今日头条")
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        fullText = response.body.decode()
        # print(fullText)
        item = SomenewItem()
        comm_re = re.search('comments_count\: (\d+)', fullText, re.S)
        if comm_re:
            item['comm_num'] = comm_re.group(1)
        else:
            item['comm_num'] = 0
        item['read_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['hot_value'] = item['comm_num']
        item['article_id'] = get_md5(response.url)
        # print(item)
        yield item









