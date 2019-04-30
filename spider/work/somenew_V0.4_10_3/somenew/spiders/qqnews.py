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

# 此爬虫爬的太快，会爬不到数据
class QqnewsSpider(scrapy.Spider):
    name = 'qqnews'
    allowed_domains = ['qq.com','news.qq.com','coral.qq.com','roll.news.qq.com','ent.qq.com']
    start_urls = ['http://ent.qq.com/articleList/rolls/']

    # 获取今日之前若干天的日期列表
    today = datetime.date.today()
    # print('*****', today)
    url_list = []
    for i in range(2):
        date = today - datetime.timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        # dates.append(date)
        # 获取新闻，娱乐，体育，财经，科技，汽车，教育，房产
        taglist = ['ent', 'sports', 'finance', 'tech','news','house','auto']
        for tag in taglist:
            for j in range(10):
                # http://roll.news.qq.com/interface/roll.php?0.7675724438699314&cata=&site=news&date=2019-03-07&page=1&mode=1&of=json
                url = 'http://roll.news.qq.com/interface/cpcroll.php?site=' + tag + '&mode=1&cata=&date=' + date + '&page={}'.format(j)
                url_list.append(url)

    def parse(self, response):

        for url in self.url_list:
            print(url)
            yield scrapy.Request(url, callback=self.parsepage, )   # dont_filter=True

    def parsepage(self, response):
        newsjson = json.loads(response.text)
        if newsjson['data']:
            # print(newsjson)
            newslist = newsjson['data']['article_info']
            for news in newslist:
                url = news['url']
                meta = {
                    'title': news['title'],
                    'pubtime': news['time'],
                }
                yield scrapy.Request(url, callback=self.parsebody,  meta=deepcopy(meta))   # dont_filter=True,
        else:
            print('没有请求到数据',response.url)

    def parsebody(self, response):
        meta = response.meta
        item = SomenewItem()
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['title'] = meta['title']
        item['url'] = response.url
        item['content'] = '\n'.join(
            response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@class='text']//text()").extract())
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['come_from'] = response.xpath("//span[@class='a_source']/a/text()").extract_first()
        item['time'] = meta['pubtime']
        item['media'] = '腾讯新闻'
        item['addr_province'] = '全国'
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        if not item['content'] == '':
            html = response.xpath("//*[@id='Main-Article-QQ']/div/div[1]/div[2]/script/text()")
            # 如果没有取到cmt_id,说明comm_num=0
            if html:
                html = html.extract_first().replace("\n", '').replace(' ', '')
                cmt_id = re.match('.*?cmt_id=(\d+).*', html).group(1)
                com_url = 'https://coral.qq.com/article/' + cmt_id + '/commentnum'
                yield scrapy.Request(com_url, callback=self.get_comm_num, dont_filter=True, meta={'item': item})
            else:
                item['comm_num'] = 0
                item['fav_num'] = '0'
                item['read_num'] = '0'
                item['env_num'] = '0'
                item['media_type'] = '网媒'
                yield item
                # print(item)

    def get_comm_num(self,response):
        item = deepcopy(response.meta['item'])
        html = response.body.decode()
        dic = json.loads(html)
        item['comm_num'] = dic['data']['commentnum']
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        # yield item
        print(item)


