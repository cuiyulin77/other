# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,re,json

class DezhouxinwenSpider(scrapy.Spider):
    # 新浪江西
    name = 'xinlangjiangxi'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp1553047223566&page=1&ch=zhengwen&cid=35688',\
                  'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp1553052137624&page=1&ch=zhengwen&cid=35694',\
                  'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp1553052195858&page=1&ch=zhengwen&cid=35689',\
                  'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp1553052418447&page=1&ch=zhengwen&cid=35687']
    def parse(self, response):
        res = re.findall(r'\((.*)',response.text)[0]
        res = json.loads(res)
        for url in res['result']['data']['list']:
            yield scrapy.Request(url['URL'], callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//*[@id=\"artibody\"]/div[2]/h1/text()").extract_first()
        item['time'] = response.xpath("//p[@class=\"source-time\"]/span[1]/text()").extract_first().replace('\xa0',' ')
        item['content'] = response.xpath('//*[@id="artibody"]/*/p/text()').extract()
        item['come_from'] =response.xpath('//*[@id="art_source"]/text()').extract()[0]
        item['content']= ''.join(item['content']).replace('\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').replace( '\r', '').replace( '\r\n', '').strip()
        if item['content'] and item['title']:
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '新浪江西'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '江西'
            yield item


