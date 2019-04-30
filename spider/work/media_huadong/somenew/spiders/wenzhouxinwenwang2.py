# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re

class DezhouxinwenSpider(scrapy.Spider):
    # 温州政府网
    name = 'wenzhouxinwenwang2'
    allowed_domains = ['wenzhou.gov.cn']
    start_urls = ['http://www.wenzhou.gov.cn/col/col1217831/index.html','http://www.wenzhou.gov.cn/col/col1217830/index.html','http://www.wenzhou.gov.cn/col/col1217832/index.html','http://www.wenzhou.gov.cn/col/col1217833/index.html','http://www.wenzhou.gov.cn/col/col1217834/index.html']
    def parse(self, response):
        print(response.url)
        r= re.findall('a href=\'(.*)\' title',response.text)
        for url in r:
            node_url = 'http://www.wenzhou.gov.cn'+url
            yield scrapy.Request(node_url, callback=self.get_detail)
        for i in range(2,20):
            i_url = response.url+'?uid=4008653&pageNum=%02d'%i
            print(i_url)
            yield scrapy.Request(i_url, callback=self.get_detail_url,dont_filter=True)
    def get_detail_url(self,response):
        print(response.url,'111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
        r= re.findall('a href=\'(.*)\' title',response.text)
        for url in r:
            node_url = 'http://www.wenzhou.gov.cn'+url
            print(node_url,'2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')
            yield scrapy.Request(node_url, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"c\"]/tr[1]/td/text()").extract_first().split('\r\n')[0]
        item['time'] = response.xpath("//*[@id=\"c\"]/tr[2]/td/table/tr/td[1]/text()").extract()[0].split('发布日期：')[1]
        item['content'] = response.xpath('//*[@id="zoom"]/p/text()').extract()
        item['come_from'] = response.xpath('//*[@id="c"]/tr[2]/td/table/tr/td[3]/text()').extract_first().split('来源：')[1]
        html_content = ''
        for i in item['content']:
            html_content += ''.join(i).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        #     item['url'] = response.url
        item['content'] = html_content
        # print(item['content'])
        print(item)
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '温州政府网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            print(item['come_from'])
            if item['come_from'] and '：'in item['come_from']:
                item['come_from'] = item['come_from'].split('：')[1]
            item['addr_province'] = '浙江'
            # print(item)
            yield item