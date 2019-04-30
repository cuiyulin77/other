# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 四川新闻网
    name = 'sichuanxinwenwang'
    allowed_domains = ['newssc.org']
    start_urls =['https://cd.scol.com.cn/cy/','http://china.newssc.org/gnjs/','http://china.newssc.org/shxw/index.shtml','http://china.newssc.org/nxw/','http://world.newssc.org/2013fyrw/','http://world.newssc.org/gjjs/','http://world.newssc.org/gj/','http://scnews.newssc.org/2009bwyc/','http://scnews.newssc.org/2009mlsh/','http://scnews.newssc.org/2009cdxw/','http://scnews.newssc.org/2009szxw/','http://world.newssc.org/gj/']
    # start_urls= ['http://local.newssc.org/szxq/index.shtml']

    def parse(self, response):
        res = response.xpath('//ul[@class="ul-listy"]/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//div[@class=\"main row\"]/div[1]/h1/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu \"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="content"]/p/text()').extract()
        item['come_from'] = response.xpath('//*[@id="source_baidu "]/a/text()').extract_first()
        if item['content'] and item['time'] and item['title']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '四川新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '四川'
            print(item)
            yield item


