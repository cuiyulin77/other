# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime
import re


# 证券日报的财经频道 http://www.zqrb.cn/finance/index.html，其他频道尚未爬取
class ZqrbCjSpider(scrapy.Spider):
    name = 'zqrb_cj'
    allowed_domains = ['zqrb.cn']
    start_urls = ['http://www.zqrb.cn/finance/index.html']

    def parse(self, response):
        # 获取分栏目
        print("1"*100)
        column_list = response.xpath("//div[@class='dhw']/ul/li/a/@href").extract()
        for column in column_list:
            yield scrapy.Request(column, callback=self.parse_detail,dont_filter=True)  # dont_filter=True

    def parse_detail(self, response):
        url_list = response.xpath("//div[@class='listMain']/ul/li/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.get_content)

    def get_content(self, response):
        item = SomenewItem()
        time_media = response.xpath("//div[@class='news_content']/div/text()").extract_first()
        try:
            item['item'] = re.match(r'\d+-\d+-\d+ \d+:\d+', time_media).group()
        except:
            item['time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['title'] = response.xpath("//div[@class='news_content']/h1/text()").extract_first()
        item['media'] = "证券日报"
        item['content'] = response.xpath("//div[@class='content']//p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
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
        yield item
