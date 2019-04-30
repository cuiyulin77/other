# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib
from copy import deepcopy
from somenew.items import SomenewItem

# 中国新闻网爬虫 http://www.chinanews.com/
class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['chinanews.com']
    start_urls = ['http://www.chinanews.com/scroll-news/news1.html']

    def parse(self, response):
        # 获取栏目列表中国新闻网
        colum_list = response.xpath("//div[@id='newsdh']/a/@href").extract()
        # 不取第一个滚动新闻，因为其他的里边都有。滚动是其他栏目的合集
        for colum in colum_list[1:]:
            url = response.urljoin(colum)
            yield scrapy.Request(url,callback=self.get_url_list)

    def get_url_list(self,response):
        li_list = response.xpath("//div[@class='content_list']/ul/li")
        for li in li_list:
            item = SomenewItem()
            href = li.xpath("./div[@class='dd_bt']/a/@href").extract_first()
            if href is not None:
                year_text = re.match(r".*?(\d{4})\/\d{2}-\d{2}\/.*",href).group(1)
                month_text = li.xpath("./div[@class='dd_time']/text()").extract_first()
                item['time'] = year_text+'-'+month_text
                item['title'] = li.xpath("./div[@class='dd_bt']/a/text()").extract_first()
                item['url'] = response.urljoin(href)
                yield scrapy.Request(item['url'],callback=self.get_content,meta={'item':deepcopy(item)})

    def get_content(self,response):
        item = response.meta['item']
        item['content'] = response.xpath("//div[@class='left_zw']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['come_from'] = response.xpath("//div[@class='left-t']/a[1]/text()").extract_first()
        if '参与互动' in item['come_from']:
            come_from = response.xpath("//div[@class='left-t']/text()").extract_first()
            come_from_re = re.search("来源：(.*)", come_from)
            if come_from_re:
                item['come_from'] = come_from_re.group(1)
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['media'] = '中国新闻网'
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        item['addr_province'] = '全国'
        yield item





