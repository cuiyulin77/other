# -*- coding: utf-8 -*-
import scrapy
import re
from somenew.utils.common import get_md5
from somenew.items import SomenewItem
from copy import deepcopy
import datetime

#======================================================================================
# 朝阳市公安局爬虫http://gaj.zgcy.gov.cn/.爬取警务资讯,政务公开,警民互动网页
#======================================================================================
class ChaoyangGonganSpider(scrapy.Spider):
    name = 'chaoyang_gongan'
    allowed_domains = ['zgcy.gov.cn','gov.cn']
    start_urls = ['http://gaj.zgcy.gov.cn/News/Jwzx/001','http://gaj.zgcy.gov.cn/News/List/002','http://gaj.zgcy.gov.cn/News/List/003']

    def parse(self, response):
        ul_list = response.xpath("//ul[@class='textlist']/li")
        for ul in ul_list:
            url = ul.xpath("./a/@href").extract_first()
            if url:
                url = response.urljoin(url)
                yield scrapy.Request(url,self.get_content)
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        next_url_re = re.match(r"\?pageIndex=(\d+)",next_url)
        if next_url_re:
            page_num = next_url_re.group(1)
            if next_url and int(page_num) <= 5:
                next_url = response.urljoin(next_url)
                # print('-2-'*20)
                yield scrapy.Request(next_url,callback=self.parse)

    def get_content(self,response):
        # print('-1-'*20)
        item = SomenewItem()
        item['title'] = response.xpath("//h1/text()").extract_first()
        meta_str = response.xpath("//div[@class='meta']/text()").extract()
        meta_str = ''.join(meta_str).replace('\r','').replace('\n','').replace(u'\xa0','').strip()
        meta_re = re.match('发布时间:(\d+\/\d+\/\d+ \d+:\d+:\d+)',meta_str)
        meta_from_re = re.search('来源：(.*)?浏览', meta_str)
        if meta_re:
            item['time'] = meta_re.group(1)
            come_from = meta_from_re.group(1)
            item['come_from'] = come_from
            content = response.xpath("//div[@class='det_content']//p//text()").extract()
            item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
            item['url'] = response.url
            item['article_id'] = get_md5(item['url'])
            item['media'] = '朝阳市公安局'
            item['media_type'] = '网媒'
            item['addr_province'] = '辽宁省'
            item['addr_city'] = '朝阳市'
            item['create_time']  = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            item['comm_num'] = 0
            item['fav_num'] = 0
            item['env_num'] = 0
            item['read_num'] = 0
            read_num_url = response.xpath("//div[@class='meta']/script/@src").extract_first()
            # print('-4/-'*20)
            if read_num_url:
                # print(read_num_url)
                yield scrapy.Request(read_num_url,callback=self.get_read_num,meta={'item':item},dont_filter=True)
            else:
                # print('-5-'*20)
                yield item

    def get_read_num(self,response):
        # print('-6-' * 20)
        item = deepcopy(response.meta['item'])
        html = response.body.decode()
        read_num_re = re.search('\d+', html)
        if read_num_re:
            # print('-7-' * 20)
            item['read_num'] = int(read_num_re.group())
            # print(item)
            yield item
        else:
            # print(item)
            yield item


