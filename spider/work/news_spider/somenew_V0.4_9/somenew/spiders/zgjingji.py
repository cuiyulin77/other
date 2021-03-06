# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import time
import datetime
from somenew.items import SomenewItem
from copy import deepcopy

# 中国经济网爬虫。http://www.ce.cn/
class ZgjingjiSpider(scrapy.Spider):
    name = 'zgjingji'
    allowed_domains = ['ce.cn']
    start_urls = ['http://www.ce.cn/xwzx/kj/index.shtml','http://www.ce.cn/xwzx/fazhi/','http://www.ce.cn/xwzx/shgj/gdxw/','http://www.ce.cn/xwzx/gnsz/szyw/','http://www.ce.cn/xwzx/gnsz/gdxw/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='sec_left']/ul/li")
        for li in li_list:
            item = SomenewItem()
            item['title'] = li.xpath(".//a/text()").extract_first()
            href = li.xpath(".//a/@href").extract_first()
            day_text = li.xpath(".//span[@class='f2']/text()").extract_first()
            if href is not None:
                try:
                    year_text = re.match(r".*?(\d{4})\d{2}\/\d{2}\/.*",href).group(1)
                    item['time'] = year_text+'/'+day_text
                except Exception as e:
                    print(e)
                url = response.urljoin(href)
                yield scrapy.Request(url,callback=self.get_content,meta={'item':deepcopy(item)})

    def get_content(self,response):
        item = response.meta['item']
        item['url'] = response.url
        item['media'] = '中国经济网'
        item['content'] = response.xpath("//div[@class='TRS_Editor']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
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
        yield item









