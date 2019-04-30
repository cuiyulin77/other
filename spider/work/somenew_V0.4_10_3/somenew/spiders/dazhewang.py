# -*- coding: utf-8 -*-
import scrapy
import datetime
import hashlib
from somenew.items import SomenewItem
import re

# ============================================
# 腾讯大浙网爬虫 首页:http://zj.qq.com/
# ============================================

class DazhewangSpider(scrapy.Spider):
    name = 'dazhewang'
    allowed_domains = ['zj.qq.com']
    start_urls = ['http://zj.qq.com/l/travel/qqy/list20120820113704.htm', 'http://zj.qq.com/l/travel/qgy/list20120820113424.htm', 'http://zj.qq.com/l/news/list20130328165910.htm', 'http://zj.qq.com/l/fashion/inhz/list20150428153509.htm', 'http://zj.qq.com/l/baby/qzzx/list20130313162320.htm', 'http://zj.qq.com/l/cul/ys/list20161123103140.htm', 'http://zj.qq.com/l/gov/list2015022815804.htm', 'http://zj.qq.com/l/finance/finance_zx/list2012092511301.htm', 'http://zj.qq.com/l/education/jyzx/list2013032810717.htm', 'http://zj.qq.com/l/health/jkzx/list20140926124402.htm', 'http://zj.qq.com/l/sports/newslist/list2016077183834.htm', 'http://zj.qq.com/l/sports/comment/list2016077181802.htm', 'http://zj.qq.com/l/education/zxx/list2016072591221.htm', 'http://zj.qq.com/l/sports/lottery/list2016077183641.htm', 'http://zj.qq.com/l/travel/zjy/list20120820113353.htm']

    def parse(self, response):
        li_list = response.xpath("//div[@class='leftList']/ul/li")
        for li in li_list:
            url = li.xpath("./a/@href").extract_first()
            yield scrapy.Request(url,callback=self.get_content)
        next_url = response.xpath('(//a[contains(text(),"下一页")])[1]/@href').extract_first()
        if next_url:
            next_num = re.match(".*?(\d+)\.htm$",next_url)
            if next_url and int(next_num.group(1))<=5:
                yield scrapy.Request(next_url,callback=self.parse)

    def get_content(self,response):
        item = {}
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['time'] = response.xpath("//span[@class='a_time']/text()").extract_first()
        if item['time'] is None:
            item['time'] = response.xpath("//span[@class='article-time']/text()").extract_first()
        item['url'] = response.url
        content = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        item['content'] = ''.join(content).replace(u'\u3000',u' ').replace(u'\xa0', u' ').replace(u'\u2022', u' ').replace('\r',' ').replace('\n',' ')
        item['create_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        m = hashlib.md5()
        url = str(item['url'])
        m.update(str(url).encode('utf8'))
        article_id = str(m.hexdigest())
        item['article_id'] = article_id
        item['come_from'] = response.xpath("//span[@class='a_source']/text()").extract_first()
        item['media'] = '腾讯大浙网'
        item['comm_num'] = '0'
        item['fav_num'] = '0'
        item['read_num'] = '0'
        item['env_num'] = '0'
        item['media_type'] = '网媒'
        item['addr_province'] = '浙江'
        yield item





