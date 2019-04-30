# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
import datetime
import time
import hashlib
from blog.items import BlogItem
from retrying import retry

class SinaBlogSpider(scrapy.Spider):
    name = 'sina_blog'
    allowed_domains = ['blog.sina.com.cn']
    start_urls = ['http://blog.sina.com.cn/lm/search/class/']

    @retry(stop_max_attempt_number=3)
    def parse(self, response):
        # 获取博客分类检索页里的博客分类
        class_list = response.xpath("//div[@class='Nav01']/a/@href").extract()
        for cls in class_list:
            yield scrapy.Request(cls,callback=self.get_blog_url)


    def get_blog_url(self,response):
        li_list = response.xpath("//div[@class='PartA']//ul/li/a/@href").extract()
        for li in li_list:
            try:
                url = re.match(r"http:\/\/blog\.sina\.com\.cn.*",li).group()
            except:
                url = None
            if url is not None:
                yield scrapy.Request(url,callback=self.get_catelog)

    # 获取博文目录链接
    def get_catelog(self,response):
        item = BlogItem()
        catelog_url = response.xpath("//*[@id='blognav']/div[2]/span[2]/a").extract_first() #博文目录链接
        item['blogger_name'] = response.xpath("//strong[@id='ownernick']/text()").extract_first() #博主名字
        yield scrapy.Request(catelog_url,callback=self.get_detail,meta={"item":item})

    def get_detail(self,response):
        item = deepcopy(response.meta['item'])
        blog_url_list = response.xpath("//div[@class='articleList']/div/p/span[2]/a/@href").extract()
        for blog_url in blog_url_list:
            item['url'] = blog_url
            yield scrapy.Request(blog_url,callback=self.get_content,meta={'item':item})

        next_url = response.xpath("//li[@class='SG_pgnext']/a/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.get_detail,meta={'item':item})

    def get_content(self,response):
        item = deepcopy(response.meta['item'])
        item['title'] = response.xpath("//h2/text()").extract_first()
        item['time'] = response.xpath("//span[@class='time SG_txtc']/text()").extract_first()
        item['time'] = item['time'].replace("(",'').replace(')','').replace('-','/')
        # sina_keyword_ad_area2
        content = response.xpath("//div[@id='sina_keyword_ad_area2']")
        # item['content'] = response.xpath("//")
        item['content'] = content[0].xpath('string(.)').extract()[0].replace('\n', '').replace('\t', ' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['media'] = '新浪博客'
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        print(item)
        yield item






