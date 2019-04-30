# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from somenew.items import SomenewItem
import hashlib
import datetime
import re

class JiaodongzaixianSpider(scrapy.Spider):
    name = 'jiaodongzaixian'
    allowed_domains = ['jiaodong.net']
    start_urls = ['http://www.jiaodong.net/','http://www.jiaodong.net/news/yantai/xianshiqu/index.html','http://www.jiaodong.net/news/','http://www.jiaodong.net/news/yantai/','http://www.jiaodong.net/news/sd/','http://www.jiaodong.net/news/china/shizheng/','http://www.jiaodong.net/news/society/','http://www.jiaodong.net/news/world/']
    # custom_settings = {'DOWNLOAD_DELAY': 20}


    def parse(self, response):
        url = ''
        res = response.xpath('//*[@id="millia"]/div[6]/div/div/div/ul/li/a/@href|//ul[@class="hotlist f14"]/li/a/@href|//*[@id="millia"]/div/div[1]/ul/li/a/@href|//*[@id="millia"]/div[8]/div[2]/ul/li/a/@href|\
//*[@id="millia"]/div[9]/div[2]/ul/li/a/@href|//div[@class="w410 fl"]/ul/li/a/@href|//*[@id="millia"]/div[19]/div[2]/ul[@class="ls01 f18 lh36 mt15"]/li/a/@href|//*[@id="millia"]/div/div/h3/a/@href').extract()
        res_url2 = response.xpath('//ul[@class="ls02 f14 lh26 clearfix"]/li/a/@href').extract()
        res_url3 = response.xpath(
            '//*[@id="millia"]/div/div/ul/li/a/@href|//*[@id="millia"]/div/div/div/ul/li/a/@href').extract()
        res_url4 = response.xpath(
            '//ul[@class="ls01 f18 lh36"]/li/a/@href|//*[@id="newsList"]/li/a/@href|//ul[@class="ls02 f14 lh26 clearfix"]/li/a/@href').extract()


        for i in (res,res_url2,res_url3,res_url4):
            if i:
                for n in i:
                    yield scrapy.Request(n, callback=self.get_detail)
                if i == res:
                    for i in range(1050,1172):
                        try:
                            url = 'http://www.jiaodong.net/news/system/count//0002001/006000000000/000/001/c0002001006000000000_00000{}.shtml'.format(i)
                        except:
                            pass
                        yield scrapy.Request(url, callback=self.get_quxian)


    def get_quxian(self,response):
        res = response.xpath('//ul[@class="ls02 f14 lh26 clearfix"]/li/a/@href').extract()
        for i in res:
            print('区县的url',i)
            yield scrapy.Request(i, callback=self.get_detail)
    def get_detail(self,response):

        item = SomenewItem()
        item['title'] = response.xpath(
            "//div[@class=\"millia\"]/h1/text()|//*[@id=\"content\"]/h1/text()|//*[@id=\"millia\"]/div/div/div/h1/text()").extract_first()
        try:
            item['time'] = response.xpath("//div[@class=\"source f14\"]/text()|//*[@id=\"content\"]/div[1]/text()|//p[@class=\"bak tc f12\"]/text()[1]").extract_first().split(
                '\u3000\u3000')[1].split('\n')[0]
        except:
            item['time'] = None
        item['url'] = response.url
        try:
            item['content'] = response.xpath(
            "//*[@id=\"content\"]/p/text()|//*[@id=\"articontent\"]/p/text()|//*[@id=\"content\"]/div/p/text()|/div[@id=\"content\"]/div/p/text()").extract()
            item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace('\xa9', u' ').replace('\n',' ').replace('\u2002', ' ').replace('\u200d', ' ').replace('\u2022', ' ').replace('\xa0', ' ').strip()
        except:
            pass
        m = hashlib.md5()
        m.update(str(item['url']).encode('utf8'))
        item['article_id'] = m.hexdigest()
        item['media'] = '胶东在线'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        try:
            item['come_from']= response.xpath("//div[@class='source f14']/text()").extract_first().split('\u3000\u3000')[0].split('来源：')[1]
        except:
            pass
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['media_type'] = '网媒'
        item['env_num'] = '0'
        item['addr_province'] = '山东省'
        item['addr_city'] = '烟台'
        print(item)
        # yield item