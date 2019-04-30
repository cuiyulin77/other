# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class ShanxixinwenwangSpider(scrapy.Spider):
    name = 'shanxixinwenwang'
    allowed_domains = ['sxrb.com']
    start_urls = ['http://news.sxrb.com/','http://www.sxrb.com/']
    def parse(self, response):
        print(len(response.url),response.url)
        if len(response.url) ==20:
            # 主页
            res = response.xpath('//*[@id="piaohong_z"]/div/div[2]/div[1]/div[3]/ul/li/a/@href\
            |//*[@id="piaohong_z"]/div/div[2]/div[2]/div/div/ul/li/a/@href\
            |//*[@id="piaohong_z"]/div/div[6]/div[1]/div[2]/div/ul/li/a/@href|//div[2]/div/div[2]/ul/li/a/@href\
            |//*[@id="b_hhwh"]/ul/ul/li/a/@href|//*[@id="b_yule"]/ul/li/a/@href|//*[@id="b_tiyu"]/ul/li/a/@href\
            |//*[@id="b_xsige"]/ul/li/a/@href').extract()
            print(len(res))
            for url in res:
                if 'http' not in url:
                    url = 'http://www.sxrb.com/'+url
                yield scrapy.Request(url, callback=self.get_detail)
        if len(response.url) == 21:
            # 新闻页面,左面标签的url提取
            res = response.xpath('/html/body/div[1]/div[4]/div[1]/div[1]/a/@href|/html/body/div[1]/div[4]/div[1]/div[3]/a/@href|/html/body/div[1]/div[5]/div/div/a/@href').extract()
            for url in res:
                if 'http' not in url:
                    url = 'http://news.sxrb.com'+url.replace('../..','')
                if 'culture' not in url:
                    yield scrapy.Request(url, callback=self.get_detail_url)
                    for i in range(2,20):
                        a = url + 'index_{}.shtml'.format(i)
                        yield scrapy.Request(a, callback=self.get_detail_url2)
    def get_detail_url2(self,response):
        """新闻页面翻页出来第一页的url"""
        res = response.xpath('/html/body/div[3]/div[2]/ul/li/a/@href').extract()
        for url in res:
            url = response.url.split('index')[0]+url[-13:]
            yield scrapy.Request(url, callback=self.get_detail)
    def get_detail_url(self,response):
        """新闻页面翻页第一页"""
        res = response.xpath('/html/body/div[3]/div[2]/ul/li/a/@href').extract()
        for url in res:
            url = response.url+url[-13:]
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[3]/p[2]/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[3]/h3/span[1]/text()').extract_first()
        item['content'] = response.xpath('/html/body/div[3]/div[4]/div[1]/p/text()|/html/body/div[3]/div[4]/div[1]/p/font/text()[2]|/html/body/div[1]/div[5]/div/div/a/@href').extract()
        item['come_from'] = response.xpath('/html/body/div[3]/h3/span[2]/text()').extract_first()

        if item['title'] and item['content']:
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['time'] = item['time'].split('时间：')[1].replace('年','/').replace('月','/').replace('日','')
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '山西新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '山西省'
            print('山西新闻网'*100)
            yield item

