# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 杭州新闻网
    name = 'hangzhouxinwenwang'
    allowed_domains = ['hangzhou.com.cn']
    start_urls = ['http://hznews.hangzhou.com.cn/','http://hznews.hangzhou.com.cn/chengshi/index.htm','http://hznews.hangzhou.com.cn/jingji/index.htm','http://hznews.hangzhou.com.cn/kejiao/index.htm','http://hznews.hangzhou.com.cn/shehui/index.htm','http://hznews.hangzhou.com.cn/wenti/index.htm']
    # start_urls = ['http://hznews.hangzhou.com.cn/jingji/index.htm']
    def parse(self, response):
        res = response.xpath('/html/body/table[3]/tr/td[1]/table[4]/tr/td/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)
        for i in range(1,16):
            url = 'http://hznews.hangzhou.com.cn/chengshi/index_{}.htm'.format(i)
            print(url)
            yield scrapy.Request(url, callback=self.get_detail_url)
        res1 = response.xpath('//td[@class="hzwNews_L_link"]/a/@href|/html/body/table[2]/tr/td[2]/table/tr/td/table/tr/td[@align="left"]/a/@href|/html/table[2]/tr/td[1]/table[5]/tr/td[1]/table/tr/td/table/tr/td/a/@href').extract()
        for url in res1:
                print(url)
                yield scrapy.Request(url, callback=self.get_detail)

    def get_detail_url(self,response):
        res = response.xpath('/html/body/table[3]/tr/td[1]/table[4]/tr/td/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url, callback=self.get_detail)

            
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        try:
            item['title']  = response.xpath("//*[@id=\"contendId\"]/table/tr/td/table[3]/tr[1]/td/table/tr[3]/td/text()").extract_first().strip('\u200b')
        except:
            item['title'] = ''
        try:
            item['time'] = response.xpath("//*[@id=\"contendId\"]/table/tr/td/table[3]/tr[1]/td/table/tr[6]/td/text()").extract()[0]
        except:
            item['time']= ''
        item['content'] = response.xpath('//p/text()').extract()
        item['come_from'] = response.xpath('//*[@id="contendId"]/table/tr/td/table[3]/tr[1]/td/table/tr[6]/td/a/text()').extract_first()
        print(item)
        html_content = ''
        for i in item['content']:
            html_content += ''.join(i).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
            item['url'] = response.url
        item['content'] = html_content
        # print(item['content'])
        if item['content'] and item['title']:

            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '杭州新闻网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            print(item['come_from'])
            item['addr_province'] = '浙江'
            print(item)
            yield item
