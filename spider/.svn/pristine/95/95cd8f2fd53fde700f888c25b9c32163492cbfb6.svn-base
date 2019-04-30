# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from somenew.items import SomenewItem
import datetime
import hashlib
import re
from time import sleep

class ZhongzhengSpider(scrapy.Spider):
    name = 'zhongzheng'
    allowed_domains = ['cs.com.cn']
    start_urls = ['http://cs.com.cn/ssgs/','http://www.cs.com.cn/gppd/','http://www.cs.com.cn/xwzx/']  #

    def parse(self, response):
        # 获取分栏目href
        column_list = response.xpath("//div[@class='ch-nav fcDBlue']//a/@href").extract()
        # column_list.append(response.url) # 吧初始url加入列表中
        for column in column_list:
            url = parse.urljoin(response.url,column)

            yield scrapy.Request(url,callback=self.get_page_list,dont_filter=True)

    def get_page_list(self,response):
        url_list = response.xpath("//ul[@class='list-lm pad10']/li/a/@href").extract()
        for url in url_list:
            url_list2 = []
            url = parse.urljoin(response.url,url)
            url_list2.append(url)
            for i in range(1,5):
                url_page = str(url) + 'index_{}.shtml'.format(i)
                url_list2.append(url_page)
            for u in url_list2:
                sleep(0.01)
                yield scrapy.Request(u,callback=self.get_content,)


    def get_content(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//div[@class='article']/h1/text()").extract_first()
        item['media'] = "中国证券报中证网"
        item['time'] = response.xpath("//div[@class='info']/p[2]/em[1]/text()").extract_first()
        item['content'] = response.xpath("//div[@class='article-t hidden']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # 暂时无法完全去除content中的网页代码，纯净的提取内容
        item['url'] = response.url
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        if item['content'] != '':
            yield item



