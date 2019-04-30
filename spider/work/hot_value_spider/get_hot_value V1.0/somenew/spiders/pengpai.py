# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
from somenew.utils.get_start_urls import get_urls
from somenew.utils.common import get_md5
import re
from copy import deepcopy
import json

# 澎湃爬虫
class PengpaiSpider(scrapy.Spider):
    name = 'pengpai'
    allowed_domains = ['thepaper.cn']
    # urls = get_urls("澎湃")
    # print(urls)
    start_urls = ['thepaper.cn']

    def start_requests(self):
        urls = get_urls("澎湃")
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        item = SomenewItem()
        url = response.url
        item['article_id'] = get_md5(url)
        com_num = response.xpath("//h2[@id='comm_span']/span/text()").extract_first()
        if com_num is None:
            com_num = 0
        else:
            com_num = com_num.replace("（", '').replace("）", '').replace("\n", '').replace("\t", '')
        com_int = re.match("(.*)k$", str(com_num))
        if com_int is not None:
            item['comm_num'] = int(float(com_int.group(1)) * 1000)
        else:
            item['comm_num'] = com_num
        item['read_num'] = '0'
        item['env_num'] = '0'
        conid = re.match('.*?(\d+)', url)
        if conid:
            conid = conid.group(1)
            fav_url = 'https://www.thepaper.cn/cont_vote_json.jsp?contid=' + str(conid)
            yield scrapy.Request(fav_url, callback=self.get_fav_num, meta={"item": item})
        else:
            item['fav_num'] = 0
            item['hot_value'] = int(item['fav_num']) + int(item['comm_num'])
            yield item

    def get_fav_num(self, response):
        item = deepcopy(response.meta['item'])
        html = response.body.decode()
        dic = json.loads(html)
        item['fav_num'] = dic['voteNum']
        item['hot_value'] = int(item['fav_num']) + int(item['comm_num'])
        yield item



