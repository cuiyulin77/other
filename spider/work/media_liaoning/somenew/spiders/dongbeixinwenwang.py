# -*- coding: utf-8 -*-
import scrapy
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime


class DongbeixinwenwangSpider(scrapy.Spider):
    name = 'dongbeixinwenwang'
    allowed_domains = ['nen.com']
    start_urls = ['http://www.nen.com.cn/','http://liaoning.nen.com.cn/hldtitle_new/']


    def parse(self, response):
        res = response.xpath('//div[not(@class="sounew")]/div[not(@class="chinas")]/ul/li/a/@href|/html/body/div[6]/div[3]/div/a/@href').extract()
        res1= response.xpath('//*[@id="h80"]/h6/a/@href').extract()
        b = []
        if  res:
            for url in res:
                if 'video' in  url:
                    b.append(url)
                elif 'xiaofei' in url:
                    b.append(url)
                elif'zfcg' in url:
                    b.append(url)
            ret_list = list(set(res) ^ set(b))
            for url in ret_list:
                yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
        if res1:
            for url in res1:
                if '011631998' not in url:
                    yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get_detail_url(self,response):
        print(response.url)
        res = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

        for i in range(1900,1945):
                url = 'http://liaoning.nen.com.cn/system/count//0008017/000000000000/000/001/c0008017000000000000_00000{}.shtml'.format(i)
                print(url)
                yield scrapy.Request(url, callback=self.get_detail_url_list, dont_filter=True)
    def get_detail_url_list(self,response):
        res = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/ul/li/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

    def get_detail(self,response):
        print(response.url)
        item = SomenewItem()
        item['title'] = response.xpath('//div/h1/text()|//html/body/div/div[4]/div[3]/div[1]/h2/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/text()|/html/body/div[5]/div/div[2]/div[3]/div[1]/text()').extract_first()
        item['content'] = response.xpath("//div[@id='rwb_zw']/span//p//text()").extract()
        # item['content'] = response.xpath('//*[@id="rwb_zw"]/ul/p/text()|//*[@id="rwb_zw"]/span[1]/p/text()').extract()
        item['come_from'] = response.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/text()|//html/body/div[5]/div/div[2]/div[3]/div[1]/text()").extract_first()
        if item['title'] and item['content'] and item['time']:
            try:
                item['time'] = item['time'].split('\xa0\xa0')[0].split('\n\n')[1].replace('年','/').replace('月','/').replace('日','')
            except:
                item['time'] = item['time'].split('\xa0\xa0')[0]
            try:
                item['come_from'] = item['come_from'].split('\xa0\xa0')[1].split('来源：')[1]
            except:
                pass
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\r', '').replace('\t','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '东北新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            print('东北新闻网' * 100)
            yield item

