# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem
import random


class RizhaoxinwenSpider(scrapy.Spider):
    name = 'rizhaoxinwen'
    allowed_domains = ['rznews.cn']
    start_urls = ['http://www.rznews.cn/','http://www.rznews.cn/viscms/xinwen6544/']
    custom_settings = {'DOWNLOAD_DELAY':0.1}

    def parse(self, response):
        res = response.xpath('//div[not(@class="bottomliebiao") and not(@class="shujishizhang") and not(@class="zhuangti") and not(@class="tjtp")]/div/ul/li/a[1]/@href').extract()
        if res:
            for url in res:
                if len(url)>40 and 'shtml'not in url and 'bbs'not in url:
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail)
        res1 = response.xpath('//div[not(@class="nav1 commWidth") and not(@class="logodh12")]/ul/li/a/@href').extract()
        if res1:
            for url in res1:
                if len(url)>46 and 'bbs'not in url:
                    print(url)
                    yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self,response):
        print('响应的url',response.url)
        item = SomenewItem()
        try:
            title = response.xpath('//div[@class="article"]/h2/span/text()|//div[@class="article"]/h2/text()').extract()
        except:
            pass
        try:
            item['time'] = response.xpath('//div[1]/div[3]/span/text()|//div[@class="article"]/span/text()').extract()[0].split('时间:')[1]
        except:
            pass
        try:
            content = response.xpath("//div[@class=\"article\"]/p/text()|//p[@style=\"TEXT-ALIGN: left\"]/span/text()").extract()
        except:
            pass
        if title and content and item['time']:
            item['title'] = ''.join(title).replace('\n','').replace('\t','').replace('\u3000','')
            item['content'] = ''.join(content).replace('\u3000','').replace('\ufeff','').replace('\xa0','')
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '日照新闻'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = '日照新闻'
            item['addr_province'] = '山东省'
            item['addr_city'] = '日照'
            yield item
            # print(item, '我是要返回的item')
