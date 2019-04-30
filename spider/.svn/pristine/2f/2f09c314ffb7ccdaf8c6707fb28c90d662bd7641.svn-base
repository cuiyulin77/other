# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 温州新闻网
    name = 'wenzhouxinwenwang'
    allowed_domains = ['news.66wz.com']
    start_urls = ['http://news.66wz.com/system/count/0002014/001000000000/000/000/c0002014001000000000_000000600.shtml']
    def parse(self, response):
        for i in range(600,687):
            res = 'http://news.66wz.com/system/count/0002014/001000000000/000/000/c0002014001000000000_000000{}.shtml'.format(i)
            yield scrapy.Request(res,callback=self.get_detail_url)
        for i in range(150, 177):
            for j in range(1,50):
                print(i,j)
                res = 'http://news.66wz.com/system/count/0002014/%03d000000000/000/000/c0002014%03d000000000_000000%d.shtml'%(j,j,i)
                yield scrapy.Request(res,callback=self.get_detail_url)
    def get_detail_url(self,response):
        res = response.xpath('//*[@id="content"]/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//*[@id=\"artibodytitle\"]/text()").extract_first()
        try:
            item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract()[0]
        except:
            item['time'] = ''
        item['content'] = response.xpath('//div[@id="artibody"]//text()').extract()
        item['come_from'] = response.xpath('//*[@id="source_baidu"]/text()').extract_first()
        html_content = ''
        for i in item['content']:
            html_content += ''.join(i).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        #     item['url'] = response.url
        item['content'] = html_content
        # print(item['content'])
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '温州新闻网'
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
            print(item)
            yield item


