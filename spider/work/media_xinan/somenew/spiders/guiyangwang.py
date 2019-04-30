# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 贵阳网
    name = 'guiyangwang'
    allowed_domains = ['gywb.cn']
    start_urls =['http://yunyan.gywb.cn/node_1304.htm','http://yunyan.gywb.cn/node_1306.htm',\
                 'http://www.gywb.cn/index_gl/node_1671.htm','http://www.gywb.cn/xinwen/node_425.htm',\
                 'http://www.gywb.cn/xinwen/node_426.htm','http://www.gywb.cn/xinwen/node_352.htm',\
                 'http://yunyan.gywb.cn/node_1304.htm','http://yunyan.gywb.cn/node_1305.htm']
    def parse(self, response):
        res =  response.xpath("//h4[@class=\"g-list-t\"]/a/@href").extract()
        for url in res:
            url = 'http://www.gywb.cn'+url[2:]
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//h1[@class=\"g-content-t text-center\"]/text()").extract_first()
        item['time'] = response.xpath("//*[@id=\"pubtime_baidu\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="g-content-c"]/p/text()').extract()
        try:
            item['come_from'] = response.xpath('//*[@id="source_baidu"]/text()').extract_first()
        except:
            item['come_from'] = ''
        if item['content'] and item['time'] and item['title']:
            item['time'] = item['time'].split('发布时间：')[1]
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '贵阳网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '贵州'
            print(item)
            yield item


