
# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 四川在线
    name = 'sichanzaixian'
    allowed_domains = ['scol.com.cn']
    start_urls =['https://sichuan.scol.com.cn/szrw/','https://sichuan.scol.com.cn/sczh/','https://cd.scol.com.cn/cdyw/','https://sichuan.scol.com.cn/fffy/','https://sichuan.scol.com.cn/ggxw/','https://sichuan.scol.com.cn/dwzw/','https://sichuan.scol.com.cn/cddt/','https://sichuan.scol.com.cn/szjh/','https://sichuan.scol.com.cn/bsyx/']
    # start_urls = ['https://sichuan.scol.com.cn/fffy/']

    def parse(self, response):
        res = response.xpath('//*[@id="txtlist"]/ul/li/a/@href|//td[@class="bt-note"]/a/@href').extract()
        for i in res:
            url = response.url[:-6]+i
            # print(url)
            # https://sichuan.scol.com.cn/fffy/201904/56854598.html
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//*[@id=\"webreal_scol_title\"]/h1/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract_first()
        item['content'] = response.xpath('//*[@id="scol_txt"]/p/text()').extract()
        item['come_from'] = response.xpath('//*[@id="source_baidu"]/a/text()').extract_first()
        if item['content'] and item['time'] and item['title']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '四川在线'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '四川'
            yield item
