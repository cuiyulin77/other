# -*- coding: utf-8 -*-
import scrapy
import scrapy
import hashlib
import datetime
from somenew.items import SomenewItem


class WeihaiSpider(scrapy.Spider):
    name = 'weihai'
    allowed_domains = ['whnews.cn']
    start_urls = ['http://www.whnews.cn/']

    def parse(self, response):
# #         主页新闻
        res = response.xpath('//div[@class="bobao_tab_bt"]/a/@href|//*[@id="body"]/div[22]/div[2]/ul/li/a/@href|//*[@id="body"]/div/div/ul/li/a/@href|//*[@id="body"]/div[29]/div/div/div[@class="home_nr"]/a/@href').extract()
        res2 = response.xpath('//ul[@class="heiti xy-topmenu-h2"]/li/a/@href').extract()
        res3 = response.xpath('//div[@class="daohang_lei daohang_xu "]/ul/li/a/@href').extract()
        for url in (res,res2,res3):
            if url:
                for i in url:
                    if 'content' in  url:
                        m  = 'http://www.whnews.cn/'+i
                        print(url,'我是url')
                        yield scrapy.Request(m, callback=self.get_detail)
                    if '2013' not in url:
                        n = 'http://www.whnews.cn/'+i
                        yield scrapy.Request(n, callback=self.get_detail_url1)
                    if 'http' not in url and '2013' not in url:
                        q= "http://www.whnews.cn/"+ i
                        print('我是发起请求的url',url)
                        yield scrapy.Request(q, callback=self.get_detail_url1)

    def get_detail_url1(self,response):
        res = response.xpath('//*[@id="d5"]/li/a/@href').extract()
        for url in res:
            if 'node' in url :
                url = 'http://www.whnews.cn/news/' + url
                if 'http' not in url and '2013' not in url:
                    url = 'http://www.whnews.cn/news/' + url
                else:
                    print('我是详情页面的url2', url)
                    yield scrapy.Request(url, callback=self.get_detail)
            else:
                url = 'http://www.whnews.cn/11zhuanti/' + url
            print('我是详情页面的url1',url)
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):

        item = SomenewItem()
        print(response.url)
        try:
            item['title'] = response.xpath('//*[@id="content"]/div[1]/h1/text()').extract_first()
        except:
            item['title'] = None

        try:
            item['time'] = response.xpath("//*[@id=\"content\"]/div[4]/div[1]/text()").extract_first().split('\r\n')[1].strip()
        except:
            item['time'] = None

        try:
            item['content'] = response.xpath('//*[@id="content"]/div[8]/p/text()').extract()
        except:
            item['content'] = None

        if item['title'] and item['content'] and item['time']:
            item['url'] = response.url
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n','').replace('\u2002', '').strip()
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '威海新闻'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['come_from'] = response.xpath('//*[@id="content"]/div[4]/div[1]/text()').extract_first().split('来源：\r\n')[1].split('\r\n   ')[0].strip()
            item['addr_province'] = '山东省'
            item['addr_city'] = '威海'
            # print(item)
            yield item