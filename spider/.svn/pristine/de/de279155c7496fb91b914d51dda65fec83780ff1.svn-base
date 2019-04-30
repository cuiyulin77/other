# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import re
import hashlib
import datetime



class XintaixinwenwangSpider(scrapy.Spider):
    name = 'xintaixinwenwang'
    allowed_domains = ['xtrb']
    start_urls = ['http://www.xtrb.cn/xt/node_1666.htm','http://www.xtrb.cn/xt/node_1784.htm',\
                  'http://www.xtrb.cn/xt/node_1667.htm','http://www.xtrb.cn/news/node_1674.htm',\
                  'http://www.xtrb.cn/news/node_1675.htm','http://news.xtrb.cn/wap/post/applist']
    # start_urls = ['http://www.xtrb.cn/news/node_1675.htm']

    def parse(self, response):
        print(len(response.url), response.url)

        # 掌上邢台
        if len(response.url) ==36:
            res = response.xpath('//*[@id="showData0"]/li/h3/a/@href').extract()
            for url in res:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
            for i in range(2,10):
                url = 'http://news.xtrb.cn/wap/post/applist?page={}'.format(i)
                yield scrapy.Request(url, callback=self.get, dont_filter=True)


        # 新闻页面
        data = re.findall(r'A href="(.*?)" target=_blank><img src="',response.text)
        for url in data:
            if len(url) ==29:
                url = response.url.split('node')[0]+url
                print(len(url),url)
                yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
        for i in range(2,10):
            url = response.url.split('.htm')[0] + '_{}.htm'.format(i)
            yield scrapy.Request(url, callback=self.get_detail_url, dont_filter=True)
    def get(self,response):
        """掌上邢台翻页详情url获取"""
        res = response.xpath('//*[@id="showData0"]/li/h3/a/@href').extract()
        for url in res:
            if len(url) == 29 :
                # url = 'http://www.xtrb.cn/xt/'+url
                print(url,'111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
            yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)

    def get_detail_url(self,response):
        """新闻页面翻页详情url获取"""
        data = re.findall(r'A href="(.*?)" target=_blank><img src="',response.text)
        for url in data:
            if len(url) == 29 :
                url = response.url.split('node')[0] + url
                print(len(url),url)
                yield scrapy.Request(url, callback=self.get_detail,dont_filter=True)
    def get_detail(self,response):
        print(response.url,'我是响应的rul')
        item= SomenewItem()
        item['title']= response.xpath('/html/body/div[4]/h1/text()').extract_first()
        item['time'] = response.xpath('/html/body/div[4]/div/div/text()').extract()[0]
        item['content'] = response.xpath('//*[@id="rwb_zw"]/p/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[4]/div/div/text()').extract()[0]

        if item['title'] and item['content']:
            item['time'] = item['time'].split('\xa0\xa0')[0].strip().split('\r\n')[0][0:19]
            print(len(item['time']))
            item['come_from'] = item['come_from'].split('\xa0\xa0')[1].strip().split('来源：')[1]
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace('\u3000', u' ').replace('\xa0', u' ').replace('\n',
                                                                                                               '').replace(
                '\u2002', '').replace('\t','').replace('\r','').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '邢台网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '河北省'
            item['addr_city'] = '邢台'
            print('邢台网'*100)
            print(item)
            yield item








