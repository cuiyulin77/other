# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime

class DezhouxinwenSpider(scrapy.Spider):
    # 东方网
    name = 'dongfangwang'
    allowed_domains = ['eastday.com']
    start_urls = ['http://news.eastday.com/eastday/gd2008/yc/index.html?t=true','http://news.eastday.com/gd2008/city/index.html','http://news.eastday.com/eastday/13news/auto/news/enjoy/index_K49.html','http://news.eastday.com/eastday/13news/auto/news/sports/index_K48.html','http://news.eastday.com/eastday/13news/auto/news/finance/index_K47.html','http://news.eastday.com/eastday/13news/auto/news/zhengfa/index_K42.html','http://news.eastday.com/gd2008/society/index.html','http://news.eastday.com/gd2008/news/index.html','http://news.eastday.com/gd2008/sh/index.html','http://news.eastday.com/eastday/13news/auto/news/pinglun/index_K43.html']
    def parse(self, response):
        res = response.xpath('//*[@id="left"]/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url,callback=self.get_detail)
        if 'gd2008' in response.url and 'news'in response.url:
            for i in range(1,7):
                url = 'http://news.eastday.com/gd2008/news/index%d.html?t=true'% i
                print(url)
                yield scrapy.Request(url, callback=self.get_detail_url)

    def get_detail_url(self,response):
        res = response.xpath('//*[@id="left"]/ul/li/a/@href').extract()
        for url in res:
            yield scrapy.Request(url,callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"gjtitle fc\"]/text()|//*[@id=\"biaoti\"]/text()").extract_first().replace('\u3000','')
        item['time'] = response.xpath("//div[@class=\"gjdata fc\"]/span[1]/text()|//*[@id=\"pubtime_baidu\"]/text()").extract()
        item['content'] = response.xpath('//*[@id="zw"]/p/text()').extract()
        item['come_from'] = response.xpath('/html/body/div[3]/div[2]/span[2]/a/text()|//*[@id="sectionleft"]/div[2]/p[2]/a/text()').extract_first()
        # print(item)
        if item['content'] and item['time'] and item['title']:
            try:
              item['time'] = item['time'][0]
              if '年'in item['time']:
                  item['time'] = item['time'].replace('年', '/').replace('月', '/').replace('年', ' ')
            except:
                item['time'] = ''
            item['time'] = item['time'][1].strip('\n').replace('年','/').replace('月','/').replace('年',' ')
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace('&nbsp',' ').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '东方网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '上海'
            print(item)
            yield item


