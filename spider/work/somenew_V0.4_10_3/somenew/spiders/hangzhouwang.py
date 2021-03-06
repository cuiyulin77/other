# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import hashlib
from somenew.items import SomenewItem

# ============================================
# 杭州网爬虫
# ============================================
class HangzhouwangSpider(scrapy.Spider):
    name = 'hangzhouwang'
    allowed_domains = ['hangzhou.com.cn']
    start_urls = ['http://news.hangzhou.com.cn/gjxw/index.htm','http://news.hangzhou.com.cn/gnxw/index.htm','http://news.hangzhou.com.cn/zjnews/index.htm','http://news.hangzhou.com.cn/jjxw/index.htm','http://news.hangzhou.com.cn/shxw/index.htm','http://hznews.hangzhou.com.cn/chengshi/index.htm','http://hznews.hangzhou.com.cn/jingji/index.htm','http://hznews.hangzhou.com.cn/kejiao/index.htm','http://hznews.hangzhou.com.cn/shehui/index.htm','http://hznews.hangzhou.com.cn/wenti/index.htm']

    def parse(self, response):

        a_list = response.xpath('//td[@align="left"]/a/@href').extract()
        for a in a_list:
            yield scrapy.Request(a,callback=self.get_content)
        next_url = response.xpath("//li[@class='page-next']/a/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)

    def get_content(self,response):
        item = SomenewItem()
        item['title'] = response.xpath('//td[@class="xwzx_wname01"]//text()').extract_first()
        time = response.xpath('//td[@class="xwzx_wname01"]/../following-sibling::tr[3]/td/text()').extract_first()
        item['time'] = time.strip(';')
        item['media'] = '杭州网'
        item['url'] = response.url
        content = response.xpath('//td[@class="xwzx_wname02"]/p//text()').extract()
        item['content'] = ''.join(content).replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u2022', u' ')
        come_from_str = response.xpath("//td[@align='right']/strong/text()").extract_first()
        come_from_str = come_from_str.replace('\xa0', '')
        come_from_re = re.search('来源：(.*)?作者', come_from_str)
        if come_from_re:
            item['come_from'] = come_from_re.group(1)
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['comm_num'] = "0"
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        item['addr_province'] = '浙江'
        item['addr_city'] = '杭州'
        yield item

























