# -*- coding: utf-8 -*-
import scrapy
import datetime
from copy import deepcopy
from somenew.utils.common import get_md5
import re

# =============================================================================
# 半岛晨报电子版爬虫 首页:http://epaper.hilizi.com/
# =============================================================================

class BandaochenbaoSpider(scrapy.Spider):
    name = 'bandaochenbao'
    allowed_domains = ['epaper.hilizi.com']
    start_urls = ['http://epaper.hilizi.com/']

    def start_requests(self):
        # 获取今日之前若干天的日期
        today = datetime.date.today()
        for i in range(15):
            date = today - datetime.timedelta(days=i)
            date = date.strftime("%Y%m%d")
            url = 'http://epaper.hilizi.com/shtml/bdcb/{}/vA01.shtml'.format(date)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        li_list = response.xpath("//div[@class='nor current']/ul/li")
        for li in li_list:
            url = li.xpath("./a/@href").extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        li_list = response.xpath("//div[@id='bm2']/ul/li")
        my_url = response.url
        'http://epaper.hilizi.com/shtml/bdcb/20181010/vA01.shtml'
        my_url_re = re.search(r'bdcb\/(\d{8})',my_url)
        if my_url_re:
            time = my_url_re.group(1)
            time = datetime.datetime.strptime(time, '%Y%m%d')
            for li in li_list:
                item = {}
                item['time'] = time
                url = li.xpath("./a/@href").extract_first()
                url = response.urljoin(url)
                item['title'] = li.xpath("./a/@title").extract_first()
                yield scrapy.Request(url,callback=self.get_content,meta={'item':item})

    def get_content(self,response):
        item = deepcopy(response.meta['item'])
        content = response.xpath("//div[@class='acon']//text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace('\n', '').replace('\r','').replace('init();','')
        item['url'] = response.url
        item['article_id'] = get_md5(item['url'])
        item['media'] = '半岛晨报'
        item['media_type'] = '报纸'
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['comm_num'] = 0
        item['fav_num'] = 0
        item['env_num'] = 0
        item['read_num'] = 0
        item['addr_province'] = '辽宁省'
        # print(item)
        yield item
