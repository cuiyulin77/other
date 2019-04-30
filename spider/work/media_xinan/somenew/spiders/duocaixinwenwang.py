# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re

class DezhouxinwenSpider(scrapy.Spider):
    # 多彩贵州
    name = 'duocaixinwenwang'
    allowed_domains = ['gog.cn']
    start_urls = ['http://news.gog.cn/newszt/index.shtml','http://news.gog.cn/gzly/index.shtml',\
                  'http://news.gog.cn/guizkj/index.shtml','http://news.gog.cn/guizcj/index.shtml',\
                  'http://news.gog.cn/guiyxw/index.shtml','http://news.gog.cn/guizwh/index.shtml',\
                  'http://news.gog.cn/guizsh/index.shtml','http://gngj.gog.cn/gn/index.shtml',\
                  'http://fc.gog.cn/fq/index.shtml','http://fc.gog.cn/cp/index.shtml',\
                  'http://fc.gog.cn/zc/index.shtml','http://news.gog.cn/guizsz/index.shtml',
                  'http://news.gog.cn/chuxlk/index.shtml']
    def parse(self, response):
        res1 = re.findall('{"abstract":(.*)}]',response.text)
        res = re.findall('\"url\":\"(.*?)\"}',res1[0])
        for i in res:
            print(i)
            yield scrapy.Request(i, callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//h1[@class=\"title\"]/text()").extract_first()
        item['time'] = response.xpath("//div[@class=\"info\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="content"]/p/text()').extract()
        item['come_from'] = response.xpath("//div[@class=\"info\"]/text()").extract_first()
        # print(item)
        if item['content'] and item['time'] and item['title']:
            item['come_from'] = item['come_from'].split('来源：')[1]
            item['time'] = item['time'].split('\u3000')[0].strip()
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '多彩贵州'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '贵州'
            print(item)
            # yield item


