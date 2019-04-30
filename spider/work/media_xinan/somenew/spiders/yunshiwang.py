# -*- coding: utf-8 -*-
import scrapy
from somenew.items import SomenewItem
import hashlib
import datetime,json

class DezhouxinwenSpider(scrapy.Spider):
    # 云视网
    name = 'yunshiwang'
    allowed_domains = ['yntv.cn']
    start_urls =['http://app.yntv.cn/front/content/content/release/blockbatchlist?sectionid=357|361&page=1&pagesize=30&_=1555399067748',\
                 'http://app.yntv.cn/front/content/content/release/blockbatchlist?sectionid=341&page=1&pagesize=30&_=1555400167205',\
                 'http://app.yntv.cn/front/content/content/release/blockbatchlist?sectionid=345&page=1&pagesize=30&_=1555400201896',\
                 'http://app.yntv.cn/front/content/content/release/blockbatchlist?sectionid=349&page=1&pagesize=30&_=1555400235500',\
                 'http://app.yntv.cn/front/content/content/release/blockbatchlist?sectionid=337&page=1&pagesize=30&_=1555400069528']

    def parse(self, response):
        res = json.loads(response.text)
        for url in res['data']['data']:
            yield scrapy.Request(url['url'],callback=self.get_detail)
    def get_detail(self,response):
        print(response.url,'响应的url')
        item = SomenewItem()
        item['title']  = response.xpath("//div[@class=\"text_title\"]/text()").extract_first()
        item['time'] = response.xpath("//span[@class=\"text_time\"]/text()").extract_first()
        item['content'] = response.xpath('//div[@class="content_left col-sm-8 col-xs-12"]/p/text()|//*[@id="layer216"]/p/text()').extract()
        try:
            item['come_from'] = response.xpath('//span[@class="text_from"]/text()').extract_first()
        except:
            item['come_from'] = ''
        if item['content'] and item['time'] and item['title']:
            item['content'] = ''.join(item['content']).replace(u'\u3000', u' ').replace(u'\xa0', u' ').\
                replace('\n', '').replace( '\u2002', '').strip()
            item['url'] = response.url
            m = hashlib.md5()
            m.update(str(item['url']).encode('utf8'))
            item['article_id'] = m.hexdigest()
            item['media'] = '云视网'
            item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = "0"
            item['fav_num'] = '0'
            item['read_num'] = '0'
            item['env_num'] = '0'
            item['media_type'] = '网媒'
            item['addr_province'] = '云南'
            yield item


