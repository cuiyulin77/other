# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem
import re
from pypinyin import pinyin,lazy_pinyin
class JiningxinwenSpider(scrapy.Spider):
    name = 'jiningxinwen'
    allowed_domains = ['jnnews.tv']
    start_urls = ['http://www.jnnews.tv/']




    def parse(self, response):

        res = response.xpath('//div[@class="lanm_list"]/ul/li/a/@href').extract()
        for url in res:
            if 'www.jnnews.tv' in url and 'jnsxwfbt' not in url:
                yield scrapy.Request(url,callback=self.get_detail_url)

    def get_detail_url(self,response):
        a = ['济宁','县区','视听','党建','视听','社会','娱乐','健康','商业']
        b = []
        for i in a:
            m = lazy_pinyin(i)
            if len(m) == 2:
                m  = str(m[0])+str(m[1])
            elif len(m) == 3:
                m = str(m[0])+str(m[1])+str(m[2])
            b.append(m)
        c = ['index',['index_'+str(i)for i in range(1,15)]]

        for i in c[1]:
            c.append(i)
        c.remove(c[1])

        res = response.xpath('//div[@class="content_tj"]/ul/li/div/a/@href').extract()
        for url in res:
            if url =='http://www.jnnews.tv/':
                yield scrapy.Request(url, callback=self.get_detail)
            else:
                for i in c:
                    for node in b:
                        url = 'http://www.jnnews.tv/{}/{}.html'.format(node,i)
                        yield scrapy.Request(url, callback=self.get_detail_url_list)
    def get_detail_url_list(self,response):
        res = response.xpath('//div[@class="content_tj"]/ul/li/div/div/h3/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        # print(response.url,'我是顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶')
        item = SomenewItem()
        try:
            item['title'] = response.xpath('//div[@class="clearfix w1000_320 text_title"]/h1/text()').extract_first()
        except:
            item['title'] = None
        try:
            item['content'] = response.xpath('//*[@id="rwb_zw"]/p/text()').extract()
        except:
            item['content'] = None
        try:
            item['time'] = response.xpath("//div[@class=\"box01\"]/div[1]/text()").extract_first().split('\xa0\xa0')[0]
            item['time'] = item['time'].replace('年','/').replace('月','/').replace('日',' ')
        except:
            item['time'] = None

        if item['title'] and item['content'] and item['time']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '济宁新闻'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] =response.xpath("//div[@class=\"box01\"]/div[1]/text()").extract_first().split('\xa0\xa0')[1].split('来源：')[1]
            item['addr_province'] = '山东省'
            item['addr_city'] = '济宁'
            yield item






