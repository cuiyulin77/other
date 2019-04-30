# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 北青网
    name = 'beiqingwang'
    allowed_domains = ['ynet.com']
    start_urls =['http://report.ynet.com/list/1179t1338.html','http://news.ynet.com/list/939t76.html',\
                 'http://news.ynet.com/list/999t76.html','http://youth.ynet.com/list/1942t2830.html',\
                 'http://youth.ynet.com/list/1948t2830.html','http://youth.ynet.com/list/1960t2830.html',\
                 'http://report.ynet.com/list/1182t1338.html','http://report.ynet.com/list/1182t1338.html',\
                 'http://report.ynet.com/list/1185t1338.html','http://report.ynet.com/list/1191t1338.html',\
                 'http://report.ynet.com/list/1203t1338.html','http://report.ynet.com/list/1209t1338.html',\
                 'http://report.ynet.com/list/1215t1338.html','http://report.ynet.com/list/1221t1338.html',\
                 'http://report.ynet.com/list/1227t1338.html','http://finance.ynet.com/list/461t815.html',\
                 'http://finance.ynet.com/list/461t815.html','http://finance.ynet.com/list/464t815.html',\
                 'http://finance.ynet.com/list/464t815.html','http://finance.ynet.com/list/467t815.html',\
                 'http://finance.ynet.com/list/2004t815.html','http://sports.ynet.com/list/735t1059.html',\
                 'http://life.ynet.com/list/564t975.html','http://home.ynet.com/list/485t914.html']

    def parse(self, response):
        res = response.xpath('//li[@class="cfix"]/h2/a/@href').extract()
        for url in res:
            print(url)
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//*[@id=\"articleContent\"]/div[1]/h1/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"yearMsg\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@id="articleBox"]/p/text()').extract()

        if item['content'] and item['time'] and item['title']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '北青网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            try:
                item['come_from'] =response.xpath('//span[@class="sourceMsg"]/text()').extract_first()
            except:
                item['come_from'] = '北青网'
            item['addr_province'] = '北京'
            item['addr_city'] ='北京'
            print(item)
            # yield item


