# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime

class HebeidianshitaiSpider(scrapy.Spider):
    name = 'hebeidianshitai'
    allowed_domains = ['hebtv.com']
    start_urls = ['http://www.hebtv.com/news/Important_news/','http://www.hebtv.com/news/people_livelihood/'\
        ,'http://www.hebtv.com/news/rule_law/','http://www.hebtv.com/news/social/',\
                  'http://www.hebtv.com/news/redian/','http://www.hebtv.com/news/entertainment/']

    def parse(self, response):
        for i  in range(1,25):
            url = response.url +'%d.shtml'%i
            yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self,response):
        res = response.xpath('//ul/li/div/a/@href').extract()
        for url  in res:
            yield scrapy.Request(url, callback=self.get_detail)


    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('//div[@class="article_title"]/h1/text()').extract_first()
        item['time'] = response.xpath('//div[2]/p[1]/text()').extract()[0]
        item['content'] = response.xpath('//article/div[1]/p/text()').extract()
        item['come_from'] = response.xpath('//div[2]/p[1]/text()').extract_first()

        if item['title'] and item['content']:

            item['come_from'] = item['come_from'].split('来源：')[1]

            item['time'] = item['time'].split('\xa0')[0].split('发布时间：')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '河北电视台'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            print('河北新闻网'*100)
            yield item



