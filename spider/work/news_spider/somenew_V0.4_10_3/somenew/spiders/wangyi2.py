# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem
from copy import deepcopy
import json
from xpinyin import Pinyin



class WangyiSpider(scrapy.Spider):
    name = 'wangyi2'
    allowed_domains = ['163.com']
    start_urls = ['http://tech.163.com/internet/','http://tech.163.com/telecom/','http://tech.163.com/it/','http://hb.news.163.com/']
    # custom_settings = {'DOWNLOAD_DELAY': 0.1}


    def parse(self, response):
        res = response.xpath('//div[@class="ls-city-cont"]/div[1]/a/@href').extract()
        for i in res:
            yield scrapy.Request(i, callback=self.get_detail_ziyuan)

        # 科技频道三个
        # res = response.xpath('//*[@id="news-flow-content"]/li/div[1]/h3/a/@href').extract()
        # for url in res:
        #     yield scrapy.Request(url, callback=self.get_detail)
        # for i in range(2,20):
        #
        #     url = 'http://tech.163.com/special/'+response.url.split('/')[-2]+'_2016_%02d/'%i
        #     yield scrapy.Request(url, callback=self.get_detail_url)
    def get_detail_ziyuan(self,response):
        url= ''
        res = response.xpath('//div[@class="newsdata_nav"]/ul/li/a/@source-url').extract_first()
        if  res is None :
            pass
        else:
            if 'http' in res:
                for i in range(1, 10):
                    if i != 1:
                        url = res.replace('.js', '_0{}.js'.format(i))
                    else:
                        url = res
            else:
                url =response.url+res
                print(url)
        yield scrapy.Request(url, callback=self.get_detail_url1)

    def get_detail_url1(self,response):
        res1 = response.body.decode(encoding='gb18030')
        res2 = res1.replace('data_callback(','').strip(')')
        try:
            res3 = json.loads(res2)
            for node in res3:
                print(node['docurl'])
                yield scrapy.Request(node['docurl'], callback=self.get_detail)
        except:
            print(response.url,'111111111111111111111111111111111111111111111111111111111111111111111111111')
            print('可能没有数据','2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="news-flow-content"]/li/div[1]/h3/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        item=SomenewItem()
        item['title'] = response.xpath("//*[@id=\"epContentLeft\"]/h1/text()").extract_first()
        item['media'] = "网易"
        item['time'] = response.xpath("//*[@id=\"epContentLeft\"]/div[1]/text()[1]").extract_first()
        item['content'] = response.xpath("//*[@id=\"endText\"]/p/text()").extract()
        item['come_from']= response.xpath("//*[@id=\"ne_article_source\"]/text()").extract_first()
        print(response.url,'我是响应的rul')
        if item['title'] and item['content']:
            item['time'] = item['time'].split('\u3000')[0].strip('\n').strip()
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '网易'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '全国'
            print('网易'*100)
            print(item)










