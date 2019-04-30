# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
from copy import deepcopy
import hashlib
from somenew.items import SomenewItem


class A21jingjiSpider(scrapy.Spider):
    name = '21jingji'
    allowed_domains = ['21jingji.com']
    url_list = ['http://www.21jingji.com/channel/business/','http://www.21jingji.com/channel/19th/','http://www.21jingji.com/channel/readnumber/','http://www.21jingji.com/channel/politics/','http://www.21jingji.com/channel/money/','http://www.21jingji.com/channel/finance/','http://www.21jingji.com/channel/BandR/','http://www.21jingji.com/channel/ftz/','http://www.21jingji.com/channel/GHM_GreaterBay/','http://www.21jingji.com/channel/herald/']
    for url in url_list:
        # 每个栏目最多只能获得10页的信息，多了返回404
        for i in range(11)[2:]:
            url_new = url+str(i)+'.html?'
            url_list.append(url_new)
    start_urls = url_list

    def parse(self, response):
        url_list = response.xpath("//div[@id='data_list']//div[@class='Tlist']/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url,callback=self.get_content)

    def get_content(self,response):
        item = SomenewItem()
        item['url'] = response.url
        item['title'] = response.xpath("//h2/text()").extract_first()
        day_text = response.xpath("//p[@class='Wh']/span[1]/text()").extract_first()
        day_new = day_text.replace('年','/').replace('月','/').replace('日',' ')
        hour_text = response.xpath("//span[@class='hour']/text()").extract_first()
        item['time'] = day_new+hour_text
        item['media'] = '21世纪经济报道'
        item['content'] = response.xpath("//div[@class='detailCont']/p//text()").extract()
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5
        url = str(item['url'])
        m.update(str(url)).encode('utf8')
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item



