# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from somenew.items import SomenewItem
import datetime
import hashlib

class ZhongzhengSpider(scrapy.Spider):
    name = 'zhongzheng'
    allowed_domains = ['cs.com.cn']
    start_urls = ['http://cs.com.cn/ssgs/','http://www.cs.com.cn/gppd/','http://www.cs.com.cn/xwzx/']

    def parse(self, response):
        # 获取分栏目href
        column_list = response.xpath("//div[@class='secbar']/span/em/a/@href").extract()
        column_list.append(response.url) # 吧初始url加入列表中
        for column in column_list:
            url = parse.urljoin(response.url,column)
            yield scrapy.Request(url,callback=self.get_page_list)

    def get_page_list(self,response):
        url_list = response.xpath("//div[@class='box740 fl']/dl/dt/a/@href").extract()
        for url in url_list:
            url = parse.urljoin(response.url,url)
            yield scrapy.Request(url,callback=self.get_content)

    def get_content(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//div[@class='artical_t']/h1/text()").extract_first()
        item['media'] = "中国证券报中证网"
        item['time'] = response.xpath("//span[@class='Ff']/text()").extract_first()
        item['content'] = response.xpath("//div[@class='artical_c']//p//text()").extract()
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
        yield item
        next_url = response.xpath("//div[@class='page']//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.get_content)


