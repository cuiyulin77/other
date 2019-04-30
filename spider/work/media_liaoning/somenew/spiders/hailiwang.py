# -*- coding: utf-8 -*-
import scrapy
from somenew.utils.common import get_md5
import datetime
import re

# =============================================================================
# 海力网爬虫 首页:http://www.hilizi.com/,和半岛晨报是同一个报社,这个非半岛晨报的报纸资讯
# =============================================================================

class HailiwangSpider(scrapy.Spider):
    name = 'hailiwang'
    allowed_domains = ['hilizi.com']
    start_urls = ['http://www.hilizi.com/html/index/dalianxinwen/','http://www.hilizi.com/html/index/focus_top/',
                  'http://www.hilizi.com/html/index/economic/','http://www.hilizi.com/html/index/shequ/',
                  'http://www.hilizi.com/html/index/yule/','http://www.hilizi.com/html/index/tiyu/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='left list']/ul/li")
        for li in li_list:
            item = {}
            item['title'] = li.xpath("./a/@title").extract_first()
            url = li.xpath("./a/@href").extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url,callback=self.parse_detail,meta={'item':item})
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        next_page = re.search(r'(\d+)\.html$', next_url)
        if next_page:
            next_page_int = int(next_page.group(1))
            if next_page_int<6:
                print('*下一页*'*30)
                print(response.urljoin(next_url))
                yield scrapy.Request(response.urljoin(next_url),callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']
        item['time'] = response.xpath("//div[@class='title']/span[3]/text()").extract_first()
        come_from = response.xpath("//div[@class='title']/span[2]/text()").extract_first()
        item['come_from'] = come_from.replace("来源：",'')
        content = response.xpath("//div[@class='content']//p//text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\x7f', u'')
        item['url'] = response.url
        item['article_id'] = get_md5(item['url'])
        item['media'] = '海力网'
        item['media_type'] = '网媒'
        item['addr_province'] = '辽宁省'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['comm_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['read_num'] = 0
        # print(item)
        yield item
