# -*- coding: utf-8 -*-
import scrapy
from somenew.utils.common import get_md5
from somenew.items import SomenewItem
from copy import deepcopy
import datetime

# =============================================================================
# 腾讯大辽网爬虫 首页:http://ln.qq.com/,汽车和房产频道爬取规则需要另写
# =============================================================================
class DaliaowangSpider(scrapy.Spider):
    name = 'daliaowang'
    allowed_domains = ['ln.qq.com']
    i = 0
    start_urls = ['http://ln.qq.com/liaoning/',
                  'http://ln.qq.com/money/','http://ln.qq.com/ent/','http://ln.qq.com/shopping/',
                  'http://ln.qq.com/travel/','http://ln.qq.com/shopping/citykitchen/','http://ln.qq.com/house/','http://ln.qq.com/life/'
                  ]

    def parse(self, response):
        div_list = response.xpath("//div[@class='text']")
        for  div in div_list:
            url = div.xpath(".//h3/a/@href").extract_first()
            if url:
                item = SomenewItem()
                url = response.urljoin(url)
                item['come_from'] = div.xpath(".//span[@class='source']/text()").extract_first()
                item['time'] = div.xpath(".//span[@class='pubtime']/text()").extract_first()
                item['title'] = div.xpath(".//h3/a/text()").extract_first()
                yield scrapy.Request(url,callback=self.get_content,meta={'item':item})

    def get_content(self,response):
        item = deepcopy(response.meta['item'])
        content = response.xpath("//div[@id='Cnt-Main-Article-QQ']//p//text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\x7f',u'')
        item['url'] = response.url
        item['article_id'] = get_md5(item['url'])
        item['media'] = '腾讯大辽网'
        item['media_type'] = '网媒'
        item['addr_province'] = '辽宁省'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['comm_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['read_num'] = 0
        yield item

