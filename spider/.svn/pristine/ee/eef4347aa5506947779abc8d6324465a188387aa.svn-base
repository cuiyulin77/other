# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class ChangchengwangSpider(scrapy.Spider):
    name = 'changchengwang'
    allowed_domains = ['hebei.com.cn']
    start_urls = ['http://www.hebei.com.cn/','http://news.hebei.com.cn/hqtp/']

    def parse(self, response):
        print(len(response.url),response.url)
        # 主页url
        res = response.xpath('//div[not(@class="ccwwq") and not(@class="ccst") and not(@class="news_right") \
        and not(@id="friendlink") and not(@class="h35px") and not(@class="threeada") and not(@class="h60px")]/div[not(@class="header clearfix") \
        and not(@class="date") and not(@class="ccwwq1") and not(@class="xmtjz")]/ul/li/a/@href|//div/ul/li/div/a/@href').extract()


        # 主页url提取
        if len(response.url) == 24:
            for url in res:
                if len(url)> 42 and 'index'not in url:
                    yield scrapy.Request(url, callback=self.get_detail)
        if len(response.url) == 30:
            # 新闻页面
            res = response.xpath('/html/body/div[4]/div/ul/li[position()>2]/a/@href').extract()
            for url in res:
                if 'news' in url:
                    yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_url(self,response):
        """新闻分类url提取"""
        res = response.xpath('//div[1]/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('//h1/text()').extract_first()
        item['time'] = response.xpath('//div[@class="post_source"]/text()').extract()
        item['come_from'] = response.xpath('//div[@class="post_source"]/text()[2]|//div[@class="post_source"]/a/text()').extract()
        item['content'] = response.xpath('//p/text()').extract()
        if item['title'] and item['content']:
            if len(item['come_from']) == 1 :
                item['come_from'] = item['come_from'][0].split('\r\n')[1].split('\n')[0]
            elif len(item['come_from']) == 2:
                item['come_from'] = item['come_from'][1]
            else:
                pass
            for node in item['time']:
                data = re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', node)
                if data:
                    item['time'] = data[0]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '长城网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            print('河北新闻网'*100)
            yield item