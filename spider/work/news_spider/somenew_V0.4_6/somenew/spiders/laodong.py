# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import hashlib
import datetime
from somenew.items import SomenewItem

# 劳动报新闻爬虫，http://www.labour-daily.cn/
# 爬取新闻头条
class LaodongSpider(scrapy.Spider):
    name = 'laodong'
    allowed_domains = ['51ldb.com']
    start_urls = ['http://www.51ldb.com/ldb/node13/node18/index.html']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='lb12']/li/a/@href").extract()
        for li in li_list:
            # href = li.xpath("//A/@href").extract_first()
            print(li)
            url = parse.urljoin(response.url,li)
            yield scrapy.Request(url,callback=self.parse_detail,dont_filter=True)
        next_url = response.xpath("//a[text()='[下页]']/@href").extract_first()
        next_url = parse.urljoin(response.url,next_url)
        if next_url is not None:
            print("+" * 100)
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_detail(self,response):
        item = SomenewItem()
        item['time'] = response.xpath("//h2[2]/text()").extract_first()
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        item['content'] = response.xpath("//ul[@class='zw']/p//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['media'] = '劳动报'
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        yield item