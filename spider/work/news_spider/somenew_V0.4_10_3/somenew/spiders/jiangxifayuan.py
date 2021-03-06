# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import hashlib
import re
import datetime
from somenew.items import SomenewItem

# 江西法院新闻中心 http://jxfy.chinacourt.org
# scrapy 默认16线程完全爬不下来东西，刚启动就停止了。改为3线程可以爬取

class JiangxifayuanSpider(scrapy.Spider):
    name = 'jiangxifayuan'
    allowed_domains = ['jxfy.chinacourt.org']
    start_urls = ['http://jxfy.chinacourt.org/article/index/id/MzAxNTAAIqIAAA%3D%3D.shtml']

    def parse(self, response):
        # 获取新闻中心栏目的分栏目url
        print("2" * 100)
        url_list = response.xpath("//div[@class='content'][1]//li/a/@href").extract()
        for url in url_list:
            print("&"*100)
            url = parse.urljoin(response.url,url)
            print("1"*100)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        href_list = response.xpath("//*[@id='main']/div[2]/ul/li//a/@href").extract()
        for href in href_list:
            url = parse.urljoin(response.url,href)
            yield scrapy.Request(url,callback=self.get_content)
        next_url = response.xpath("(//a[text()='下一页'])[1]/@href").extract_first()
        next_url = parse.urljoin(response.url,next_url)
        if next_url is not None:
            yield scrapy.Request(next_url,callback = self.parse_detail)

    def get_content(self,response):
        item = SomenewItem()
        item['title'] = response.xpath("//div[@class='b_title']/text()").extract_first()
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='text']//text()").extract()
        item['content'] = ''.join(item["content"]).replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        # 江西法院没体现信息来源
        time_text = response.xpath("//div[@class='sth_a']/span/text()").extract_first()
        try:
            item['time'] = re.match(r".*?(\d+-\d+-\d+\s+\d+:\d+:\d+)\s+",time_text).group(1)
        except:
            item['time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['media'] = '江西法院'
        # 创建时间
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
        item['addr_province'] = '江西'
        yield item